"""Couleurs unies par tag pour la vignette des articles.

Dérivées des 8 teintes catégorielles validées (cf. skill dataviz) : chaque
famille de tags partage une teinte, déclinée en 3-4 nuances (base/tint/shade)
pour couvrir les tags sans recourir à une hue générée à la volée. Les
articles sans tag utilisent une couleur neutre dédiée plutôt qu'une teinte
de la palette catégorielle (pour ne jamais être confondus avec un vrai tag).

Data et Tutorial ont été déplacés hors de leur famille d'origine (trop
proches visuellement de Security) vers les familles jaune et violette, qui
avaient un créneau libre. Le tag AI / Machine Learning a été retiré : les
articles liés à l'IA sont exclus du dashboard (cf. tags.py::is_ai_related).
"""

NO_TAG_COLOR = {"light": "#898781", "dark": "#898781"}

TAG_COLORS = {
    # famille bleu — langages
    "Python": {"light": "#2a78d6", "dark": "#3987e5"},
    "JavaScript": {"light": "#6aa0e2", "dark": "#74abed"},
    "Go": {"light": "#215ea7", "dark": "#2c69b3"},
    "Rust": {"light": "#9fc2ed", "dark": "#a6c9f3"},

    # famille orange — systèmes bas niveau / recherche
    "Systems / Low-level": {"light": "#eb6834", "dark": "#d95926"},
    "Research": {"light": "#b75129", "dark": "#a9451e"},

    # famille aqua — cloud / infra
    "Cloud": {"light": "#1baf7a", "dark": "#199e70"},
    "DevOps": {"light": "#5fc7a2", "dark": "#5ebb9b"},
    "Database": {"light": "#15885f", "dark": "#147b57"},
    "API": {"light": "#98dbc3", "dark": "#98d3bf"},

    # famille jaune — web / design / data
    "Web": {"light": "#eda100", "dark": "#c98500"},
    "Design": {"light": "#f2bd4c", "dark": "#d9aa4c"},
    "Open Source": {"light": "#b97e00", "dark": "#9d6800"},
    "Data": {"light": "#f7d58c", "dark": "#e7c88c"},

    # famille magenta — business / people
    "Startup / Business": {"light": "#e87ba4", "dark": "#d55181"},
    "Career": {"light": "#efa3bf", "dark": "#e285a7"},
    "Gaming": {"light": "#b56080", "dark": "#a63f65"},

    # famille verte — systèmes / perf
    "Linux": {"light": "#008300", "dark": "#008300"},
    "Performance": {"light": "#4ca84c", "dark": "#4ca84c"},
    "Robotics / Hardware": {"light": "#006600", "dark": "#006600"},

    # famille violette — mobile / 3D / blockchain / tutoriels
    "Mobile": {"light": "#4a3aa7", "dark": "#9085e9"},
    "3D / Graphics": {"light": "#8075c1", "dark": "#b1aaf0"},
    "Blockchain": {"light": "#3a2d82", "dark": "#7068b6"},
    "Tutorial": {"light": "#aea6d7", "dark": "#cdc8f5"},

    # famille rouge — sécurité / vie privée / espace / algo
    "Security": {"light": "#e34948", "dark": "#e66767"},
    "Privacy": {"light": "#eb807f", "dark": "#ee9595"},
    "Space": {"light": "#b13938", "dark": "#b35050"},
    "Algorithms / CS Theory": {"light": "#f2adad", "dark": "#f4bbbb"},
}


def color_for(tags: list[str], dark_mode: bool) -> str:
    """Couleur unie pour la vignette d'un article : celle du premier tag,
    ou la couleur neutre "aucun tag" si la liste est vide."""
    mode = "dark" if dark_mode else "light"
    if not tags:
        return NO_TAG_COLOR[mode]
    return TAG_COLORS.get(tags[0], NO_TAG_COLOR)[mode]
