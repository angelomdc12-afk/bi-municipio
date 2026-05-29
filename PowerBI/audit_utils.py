import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from collections.abc import Mapping

BASE_DIR = Path(__file__).resolve().parent


def _secrets_audit_cfg():
    try:
        import streamlit as st

        audit_cfg = st.secrets.get("audit", {})
        return audit_cfg if isinstance(audit_cfg, Mapping) else {}
    except Exception:
        return {}


def _resolve_audit_file():
    """Resolve caminho do arquivo de auditoria com prioridade por configuracao."""
    env_file = os.getenv("AUDIT_FILE", "").strip()
    if env_file:
        return Path(env_file).expanduser().resolve()

    env_dir = os.getenv("AUDIT_DIR", "").strip()
    if env_dir:
        return (Path(env_dir).expanduser().resolve() / "access_audit.csv")

    audit_cfg = _secrets_audit_cfg()
    secret_file = str(audit_cfg.get("store_file", "")).strip()
    if secret_file:
        return Path(secret_file).expanduser().resolve()

    secret_dir = str(audit_cfg.get("store_dir", "")).strip()
    if secret_dir:
        return (Path(secret_dir).expanduser().resolve() / "access_audit.csv")

    mount_data = Path("/mount/data")
    if mount_data.exists() and mount_data.is_dir():
        return (mount_data / "bi-municipio" / "access_audit.csv").resolve()

    return (BASE_DIR / "logs" / "access_audit.csv").resolve()

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
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_audit_event(event, user="", page="", session_id="", details=""):
    """Registra eventos de auditoria sem interromper o app em caso de erro."""
    try:
        audit_file = _resolve_audit_file()
        audit_dir = audit_file.parent
        audit_dir.mkdir(parents=True, exist_ok=True)
        write_header = (not audit_file.exists()) or audit_file.stat().st_size == 0

        payload = {
            "timestamp": _timestamp_iso_local(),
            "event": _safe_text(event),
            "user": _safe_text(user),
            "page": _safe_text(page),
            "session_id": _safe_text(session_id),
            "details": _safe_text(details),
        }

        with audit_file.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            if write_header:
                writer.writeheader()
            writer.writerow(payload)

        return True
    except Exception:
        return False


def read_audit_events(limit=1000):
    """Retorna eventos mais recentes de auditoria em ordem decrescente."""
    try:
        audit_file = _resolve_audit_file()
        if not audit_file.exists() or audit_file.stat().st_size == 0:
            return []

        with audit_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        if limit and limit > 0:
            rows = rows[-limit:]

        rows.reverse()
        return rows
    except Exception:
        return []
