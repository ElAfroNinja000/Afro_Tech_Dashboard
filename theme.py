"""Palettes clair/sombre pour le thème togglable de l'app, alignées sur les
rôles "chrome & ink" de la palette de référence (surface, ink, bordure)."""

LIGHT = {
    "app_bg": "#f9f9f7",
    "sidebar_bg": "#fcfcfb",
    "card_bg": "#ffffff",
    "card_border": "rgba(11,11,11,0.10)",
    "text": "#0b0b0b",
    "muted_text": "#52514e",
    "pill_bg": "rgba(11,11,11,0.06)",
}

DARK = {
    "app_bg": "#0d0d0d",
    "sidebar_bg": "#1a1a19",
    "card_bg": "#1a1a19",
    "card_border": "rgba(255,255,255,0.10)",
    "text": "#ffffff",
    "muted_text": "#c3c2b7",
    "pill_bg": "rgba(255,255,255,0.08)",
}


def get(dark_mode: bool) -> dict:
    return DARK if dark_mode else LIGHT
