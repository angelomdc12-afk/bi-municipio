import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from collections.abc import Mapping
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent


def _mount_audit_file():
    mount_data = Path("/mount/data")
    if mount_data.exists() and mount_data.is_dir():
        return (mount_data / "bi-municipio" / "access_audit.csv").resolve()
    return None


def _is_repo_managed_path(file_path):
    try:
        return file_path.resolve().is_relative_to(REPO_ROOT.resolve())
    except Exception:
        return False


def _prefer_persistent_audit_path(candidate_file):
    # Em cloud com volume, evita gravar auditoria em caminho do repo.
    mount_file = _mount_audit_file()
    if mount_file and _is_repo_managed_path(candidate_file):
        return mount_file
    return candidate_file


def _secrets_audit_cfg():
    try:
        import streamlit as st

        audit_cfg = st.secrets.get("audit", {})
        return audit_cfg if isinstance(audit_cfg, Mapping) else {}
    except Exception:
        return {}


def _resolve_audit_timezone():
    """Resolve timezone da auditoria com prioridade por configuracao."""
    env_tz = os.getenv("AUDIT_TIMEZONE", "").strip()
    if env_tz:
        return env_tz

    audit_cfg = _secrets_audit_cfg()
    secret_tz = str(audit_cfg.get("timezone", "")).strip()
    if secret_tz:
        return secret_tz

    # Padrao do projeto: horario de Brasilia.
    return "America/Sao_Paulo"


def _resolve_audit_file():
    """Resolve caminho do arquivo de auditoria com prioridade por configuracao."""
    env_file = os.getenv("AUDIT_FILE", "").strip()
    if env_file:
        return _prefer_persistent_audit_path(Path(env_file).expanduser().resolve())

    env_dir = os.getenv("AUDIT_DIR", "").strip()
    if env_dir:
        return _prefer_persistent_audit_path((Path(env_dir).expanduser().resolve() / "access_audit.csv"))

    audit_cfg = _secrets_audit_cfg()
    secret_file = str(audit_cfg.get("store_file", "")).strip()
    if secret_file:
        return _prefer_persistent_audit_path(Path(secret_file).expanduser().resolve())

    secret_dir = str(audit_cfg.get("store_dir", "")).strip()
    if secret_dir:
        return _prefer_persistent_audit_path((Path(secret_dir).expanduser().resolve() / "access_audit.csv"))

    mount_file = _mount_audit_file()
    if mount_file:
        return mount_file

    try:
        return (Path.home() / ".bi-municipio" / "access_audit.csv").resolve()
    except Exception:
        pass

    return (BASE_DIR / "logs" / "access_audit.csv").resolve()


def _fallback_audit_files(primary_file):
    candidates = []

    mount_file = _mount_audit_file()
    if mount_file:
        candidates.append(mount_file)

    try:
        candidates.append((Path.home() / ".bi-municipio" / "access_audit.csv").resolve())
    except Exception:
        pass

    candidates.append((BASE_DIR / "logs" / "access_audit.csv").resolve())

    unique = []
    seen = set()
    for file_path in candidates:
        key = str(file_path)
        if key in seen or key == str(primary_file):
            continue
        seen.add(key)
        unique.append(file_path)
    return unique


def _audit_file_rank(file_path, primary_file):
    mount_file = _mount_audit_file()
    try:
        resolved_file = file_path.resolve()
    except Exception:
        resolved_file = file_path

    try:
        resolved_primary = primary_file.resolve()
    except Exception:
        resolved_primary = primary_file

    if mount_file and resolved_file == mount_file:
        return 0
    if resolved_file == resolved_primary and not _is_repo_managed_path(resolved_file):
        return 1
    if not _is_repo_managed_path(resolved_file):
        return 2
    return 4

FIELDNAMES = [
    "timestamp",
    "event",
    "user",
    "page",
    "session_id",
    "details",
]


def _safe_text(value):
    if value is None:
        return ""
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def _timestamp_iso_local():
    try:
        tz_name = _resolve_audit_timezone()
        return datetime.now(ZoneInfo(tz_name)).isoformat(timespec="seconds")
    except Exception:
        # Fallback defensivo caso timezone configurado seja invalido.
        return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_audit_event(event, user="", page="", session_id="", details=""):
    """Registra eventos de auditoria sem interromper o app em caso de erro."""
    try:
        payload = {
            "timestamp": _timestamp_iso_local(),
            "event": _safe_text(event),
            "user": _safe_text(user),
            "page": _safe_text(page),
            "session_id": _safe_text(session_id),
            "details": _safe_text(details),
        }

        audit_file = _resolve_audit_file()
        target_files = [audit_file] + _fallback_audit_files(audit_file)

        wrote_any = False
        for target_file in target_files:
            try:
                target_dir = target_file.parent
                target_dir.mkdir(parents=True, exist_ok=True)
                write_header = (not target_file.exists()) or target_file.stat().st_size == 0
                with target_file.open("a", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
                    if write_header:
                        writer.writeheader()
                    writer.writerow(payload)
                wrote_any = True
            except Exception:
                continue

        return wrote_any
    except Exception:
        return False


def read_audit_events(limit=1000):
    """Retorna eventos mais recentes de auditoria em ordem decrescente."""
    try:
        audit_file = _resolve_audit_file()
        read_candidates = []
        seen = set()
        for candidate in [audit_file] + _fallback_audit_files(audit_file):
            key = str(candidate)
            if key in seen:
                continue
            seen.add(key)
            read_candidates.append(candidate)

        existing_candidates = [
            p for p in read_candidates if p.exists() and p.stat().st_size > 0
        ]
        if not existing_candidates:
            return []

        best_audit_file = min(
            existing_candidates,
            key=lambda p: (_audit_file_rank(p, audit_file), -p.stat().st_mtime),
        )

        with best_audit_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        if limit and limit > 0:
            rows = rows[-limit:]

        rows.reverse()
        return rows
    except Exception:
        return []
