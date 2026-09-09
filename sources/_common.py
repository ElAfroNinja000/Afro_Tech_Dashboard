"""Utilitaires partagés entre les différentes sources."""
from datetime import datetime, timezone
import time


def to_iso(struct_time_or_dt=None, unix_ts=None, iso_string=None, fallback_now=True) -> str:
    """Normalise une date (struct_time de feedparser, timestamp unix ou string ISO)
    vers un format ISO 8601 triable lexicographiquement (YYYY-MM-DDTHH:MM:SS)."""
    try:
        if iso_string:
            # feedparser / API renvoient déjà souvent de l'ISO 8601 (avec ou sans 'Z')
            return datetime.fromisoformat(iso_string.replace("Z", "+00:00")).strftime("%Y-%m-%dT%H:%M:%S")
        if unix_ts is not None:
            return datetime.fromtimestamp(unix_ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        if struct_time_or_dt is not None:
            return datetime.fromtimestamp(time.mktime(struct_time_or_dt), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError, OverflowError):
        pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") if fallback_now else ""
