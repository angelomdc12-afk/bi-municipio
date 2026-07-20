import hashlib
import hmac
import json
import os
import secrets
from collections.abc import Mapping
from pathlib import Path

import streamlit as st

PBKDF2_PREFIX = "pbkdf2_sha256"
PBKDF2_ITERATIONS = 390000

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent


def _mount_auth_store_file():
    mount_data = Path("/mount/data")
    if mount_data.exists() and mount_data.is_dir():
        return (mount_data / "bi-municipio" / "auth_store.json").resolve()
    return None


def _is_repo_managed_path(file_path):
    try:
        return file_path.resolve().is_relative_to(REPO_ROOT.resolve())
    except Exception:
        return False


def _prefer_persistent_store_path(candidate_file):
    # Em cloud com volume, evita gravar em caminhos do repo (volateis em deploy).
    mount_file = _mount_auth_store_file()
    if mount_file and _is_repo_managed_path(candidate_file):
        return mount_file
    return candidate_file


def _secrets_auth_cfg():
    try:
        auth_cfg = st.secrets.get("auth", {})
        return auth_cfg if isinstance(auth_cfg, Mapping) else {}
    except Exception:
        return {}


def _resolve_auth_store_file():
    """Resolve caminho do arquivo de persistencia com prioridade por configuracao."""
    # 1) Variavel de ambiente para arquivo completo
    env_file = os.getenv("AUTH_STORE_FILE", "").strip()
    if env_file:
        return _prefer_persistent_store_path(Path(env_file).expanduser().resolve())

    # 2) Variavel de ambiente para diretorio
    env_dir = os.getenv("AUTH_STORE_DIR", "").strip()
    if env_dir:
        return _prefer_persistent_store_path((Path(env_dir).expanduser().resolve() / "auth_store.json"))

    # 3) Secrets (streamlit) para arquivo completo ou diretorio
    auth_cfg = _secrets_auth_cfg()
    secret_file = str(auth_cfg.get("store_file", "")).strip()
    if secret_file:
        return _prefer_persistent_store_path(Path(secret_file).expanduser().resolve())

    secret_dir = str(auth_cfg.get("store_dir", "")).strip()
    if secret_dir:
        return _prefer_persistent_store_path((Path(secret_dir).expanduser().resolve() / "auth_store.json"))

    # 4) Em ambiente cloud, prioriza volume de dados se existir
    mount_file = _mount_auth_store_file()
    if mount_file:
        return mount_file

    # 5) Fallback para diretório de usuário (fora do repo, menos sujeito a reset por git pull)
    try:
        return (Path.home() / ".bi-municipio" / "auth_store.json").resolve()
    except Exception:
        pass

    # 6) Último fallback local no projeto
    return (BASE_DIR / "logs" / "auth_store.json").resolve()


def _fallback_auth_store_files(primary_file):
    """Lista caminhos de espelho para redundancia de persistencia."""
    candidates = []

    mount_file = _mount_auth_store_file()
    if mount_file:
        candidates.append(mount_file)

    try:
        candidates.append((Path.home() / ".bi-municipio" / "auth_store.json").resolve())
    except Exception:
        pass

    candidates.append((BASE_DIR / "logs" / "auth_store.json").resolve())

    unique = []
    seen = set()
    for file_path in candidates:
        key = str(file_path)
        if key in seen or key == str(primary_file):
            continue
        seen.add(key)
        unique.append(file_path)
    return unique


def _store_file_rank(file_path, primary_file):
    """Menor valor = fonte mais confiavel para leitura."""
    mount_file = _mount_auth_store_file()
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


def _is_deploy_persistent_store(file_path):
    """True quando o store está em volume persistente de deploy (/mount/data)."""
    mount_file = _mount_auth_store_file()
    if not mount_file:
        return False

    try:
        return file_path.resolve() == mount_file.resolve()
    except Exception:
        return False


def _default_store():
    return {
        "users": {},
        "permissions": {},
        "disabled_users": [],
    }


def _normalize_username(username):
    return str(username or "").strip()


def _read_store():
    payload = _default_store()
    try:
        auth_store_file = _resolve_auth_store_file()

        read_candidates = []
        seen = set()
        for candidate in [auth_store_file] + _fallback_auth_store_files(auth_store_file):
            key = str(candidate)
            if key in seen:
                continue
            seen.add(key)
            read_candidates.append(candidate)

        existing_candidates = [
            p for p in read_candidates if p.exists() and p.stat().st_size > 0
        ]
        if not existing_candidates:
            return payload

        # Prioriza fonte persistente (ex.: /mount/data); usa mtime como desempate.
        best_store_file = min(
            existing_candidates,
            key=lambda p: (_store_file_rank(p, auth_store_file), -p.stat().st_mtime),
        )

        raw = json.loads(best_store_file.read_text(encoding="utf-8"))
        if not isinstance(raw, Mapping):
            return payload

        users_raw = raw.get("users", {})
        if isinstance(users_raw, Mapping):
            for username, value in users_raw.items():
                username_text = _normalize_username(username)
                if username_text and isinstance(value, str) and value.strip():
                    payload["users"][username_text] = value.strip()

        permissions_raw = raw.get("permissions", {})
        if isinstance(permissions_raw, Mapping):
            for username, pages_raw in permissions_raw.items():
                username_text = _normalize_username(username)
                if not username_text:
                    continue
                pages = _normalize_permission_pages(pages_raw)
                if pages:
                    payload["permissions"][username_text] = pages

        disabled_raw = raw.get("disabled_users", [])
        if isinstance(disabled_raw, list):
            seen = set()
            normalized = []
            for username in disabled_raw:
                username_text = _normalize_username(username)
                if username_text and username_text not in seen:
                    seen.add(username_text)
                    normalized.append(username_text)
            payload["disabled_users"] = normalized

        return payload
    except Exception:
        return payload


def _write_store(payload):
    try:
        auth_store_file = _resolve_auth_store_file()
        target_files = [auth_store_file] + _fallback_auth_store_files(auth_store_file)
        content = json.dumps(payload, ensure_ascii=False, indent=2)

        wrote_any = False
        for target_file in target_files:
            try:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                tmp_file = target_file.with_suffix(target_file.suffix + ".tmp")
                tmp_file.write_text(content, encoding="utf-8")
                tmp_file.replace(target_file)
                wrote_any = True
            except Exception:
                # Mantem robustez: tenta demais destinos sem quebrar a operacao.
                continue

        if not wrote_any:
            return False
        return True
    except Exception:
        return False


def hash_password(password, iterations=PBKDF2_ITERATIONS):
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        str(password).encode("utf-8"),
        salt,
        int(iterations),
    ).hex()
    return f"{PBKDF2_PREFIX}${int(iterations)}${salt.hex()}${derived}"


def set_user_password(username, raw_password):
    username_text = _normalize_username(username)
    if not username_text:
        return False
    password_hash = hash_password(raw_password)

    store = _read_store()
    store["users"][username_text] = password_hash
    store["disabled_users"] = [u for u in store["disabled_users"] if u != username_text]
    return _write_store(store)


def set_user_permissions(username, pages):
    username_text = _normalize_username(username)
    if not username_text:
        return False

    normalized_pages = _normalize_permission_pages(pages)
    store = _read_store()
    if normalized_pages:
        store["permissions"][username_text] = normalized_pages
    else:
        store["permissions"].pop(username_text, None)
    store["disabled_users"] = [u for u in store["disabled_users"] if u != username_text]
    return _write_store(store)


def disable_user(username):
    username_text = _normalize_username(username)
    if not username_text:
        return False

    store = _read_store()
    store["users"].pop(username_text, None)
    store["permissions"].pop(username_text, None)
    if username_text not in store["disabled_users"]:
        store["disabled_users"].append(username_text)
    return _write_store(store)


def read_auth_store_summary():
    auth_store_file = _resolve_auth_store_file()
    store = _read_store()
    store_is_deploy_persistent = _is_deploy_persistent_store(auth_store_file)
    return {
        "users": dict(store.get("users", {})),
        "permissions": dict(store.get("permissions", {})),
        "disabled_users": list(store.get("disabled_users", [])),
        "store_path": str(auth_store_file),
        "store_exists": auth_store_file.exists(),
        "store_is_deploy_persistent": store_is_deploy_persistent,
    }


def verify_password(password, stored_value):
    """Valida senha em formato PBKDF2 ou formato legado em texto puro."""
    if not isinstance(stored_value, str):
        return False

    if stored_value.startswith("plain$"):
        return hmac.compare_digest(stored_value[len("plain$"):], password)

    parts = stored_value.split("$")
    if len(parts) == 4 and parts[0] == PBKDF2_PREFIX:
        try:
            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            expected = parts[3]
        except Exception:
            return False

        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        ).hex()
        return hmac.compare_digest(derived, expected)

    return hmac.compare_digest(stored_value, password)


def _flatten_toml_mapping(raw, parent_key="", separator="."):
    if not isinstance(raw, Mapping):
        return raw

    flattened = {}
    for key, value in raw.items():
        key_text = str(key)
        new_key = f"{parent_key}{separator}{key_text}" if parent_key else key_text
        if isinstance(value, Mapping):
            flattened.update(_flatten_toml_mapping(value, new_key, separator))
        else:
            flattened[new_key] = value
    return flattened


def load_auth_users_from_secrets():
    auth_cfg = st.secrets.get("auth", {})
    users_cfg = auth_cfg.get("users", {}) if isinstance(auth_cfg, Mapping) else {}
    users_cfg = _flatten_toml_mapping(users_cfg)

    users = {}
    for username, cfg in users_cfg.items():
        if isinstance(cfg, str):
            users[str(username)] = cfg
            continue

        if isinstance(cfg, Mapping):
            password_value = cfg.get("password_hash") or cfg.get("password")
            if password_value:
                users[str(username)] = str(password_value)

    store = _read_store()
    for username in store.get("disabled_users", []):
        users.pop(username, None)

    for username, password_hash in store.get("users", {}).items():
        users[username] = password_hash

    return users


def _normalize_permission_pages(raw_pages):
    if isinstance(raw_pages, str):
        return [raw_pages.strip()] if raw_pages.strip() else []

    if isinstance(raw_pages, (list, tuple)):
        normalized = []
        for page in raw_pages:
            page_text = str(page).strip()
            if page_text:
                normalized.append(page_text)
        return normalized

    return []


def load_permissions_from_secrets(default_permissions):
    auth_cfg = st.secrets.get("auth", {})
    permissions_cfg = auth_cfg.get("permissions", {}) if isinstance(auth_cfg, Mapping) else {}
    permissions_cfg = _flatten_toml_mapping(permissions_cfg)

    merged_permissions = {}
    for username, pages in (default_permissions or {}).items():
        username_text = _normalize_username(username)
        normalized_pages = _normalize_permission_pages(pages)
        if username_text and normalized_pages:
            merged_permissions[username_text] = normalized_pages

    if isinstance(permissions_cfg, Mapping):
        for username, raw_value in permissions_cfg.items():
            username_text = _normalize_username(username)
            if not username_text:
                continue

            if isinstance(raw_value, Mapping):
                pages = _normalize_permission_pages(raw_value.get("pages", []))
            else:
                pages = _normalize_permission_pages(raw_value)

            if pages:
                merged_permissions[username_text] = pages

    store = _read_store()
    for username in store.get("disabled_users", []):
        merged_permissions.pop(username, None)

    for username, pages in store.get("permissions", {}).items():
        normalized_pages = _normalize_permission_pages(pages)
        if normalized_pages:
            merged_permissions[username] = normalized_pages

    return merged_permissions or (default_permissions or {})
