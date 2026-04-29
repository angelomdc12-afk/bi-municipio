import hashlib
import hmac
import json
import secrets
from collections.abc import Mapping
from pathlib import Path

import streamlit as st

PBKDF2_PREFIX = "pbkdf2_sha256"
PBKDF2_ITERATIONS = 390000

BASE_DIR = Path(__file__).resolve().parent
AUTH_STORE_DIR = BASE_DIR / "logs"
AUTH_STORE_FILE = AUTH_STORE_DIR / "auth_store.json"


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
        if not AUTH_STORE_FILE.exists() or AUTH_STORE_FILE.stat().st_size == 0:
            return payload

        raw = json.loads(AUTH_STORE_FILE.read_text(encoding="utf-8"))
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
        AUTH_STORE_DIR.mkdir(parents=True, exist_ok=True)
        AUTH_STORE_FILE.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
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
    store = _read_store()
    return {
        "users": dict(store.get("users", {})),
        "permissions": dict(store.get("permissions", {})),
        "disabled_users": list(store.get("disabled_users", [])),
        "store_path": str(AUTH_STORE_FILE),
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


def load_auth_users_from_secrets():
    auth_cfg = st.secrets.get("auth", {})
    users_cfg = auth_cfg.get("users", {}) if isinstance(auth_cfg, Mapping) else {}

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
