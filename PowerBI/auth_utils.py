import hashlib
import hmac
from collections.abc import Mapping

import streamlit as st

PBKDF2_PREFIX = "pbkdf2_sha256"


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

    if not isinstance(permissions_cfg, Mapping) or not permissions_cfg:
        return default_permissions

    parsed_permissions = {}
    for username, raw_value in permissions_cfg.items():
        username_text = str(username).strip()
        if not username_text:
            continue

        if isinstance(raw_value, Mapping):
            pages = _normalize_permission_pages(raw_value.get("pages", []))
        else:
            pages = _normalize_permission_pages(raw_value)

        if pages:
            parsed_permissions[username_text] = pages

    return parsed_permissions or default_permissions
