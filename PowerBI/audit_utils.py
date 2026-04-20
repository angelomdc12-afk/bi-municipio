import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIT_DIR = BASE_DIR / "logs"
AUDIT_FILE = AUDIT_DIR / "access_audit.csv"

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
        AUDIT_DIR.mkdir(parents=True, exist_ok=True)
        write_header = (not AUDIT_FILE.exists()) or AUDIT_FILE.stat().st_size == 0

        payload = {
            "timestamp": _timestamp_iso_local(),
            "event": _safe_text(event),
            "user": _safe_text(user),
            "page": _safe_text(page),
            "session_id": _safe_text(session_id),
            "details": _safe_text(details),
        }

        with AUDIT_FILE.open("a", encoding="utf-8", newline="") as handle:
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
        if not AUDIT_FILE.exists() or AUDIT_FILE.stat().st_size == 0:
            return []

        with AUDIT_FILE.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        if limit and limit > 0:
            rows = rows[-limit:]

        rows.reverse()
        return rows
    except Exception:
        return []
