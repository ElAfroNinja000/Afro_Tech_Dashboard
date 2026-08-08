import streamlit as st

import theme
from tag_colors import color_for
from db import init_db, save_articles, get_articles, get_all_tags
from sources import fetch_all_articles

REFRESH_TTL_SECONDS = 30 * 60  # auto-refresh sources at most every 30 minutes

st.set_page_config(page_title="Tech Watch", page_icon="🚀", layout="wide")

# le toggle est rendu en premier pour que sa valeur de retour (fraîche pour
# cette exécution) pilote le thème injecté juste après — lire
# st.session_state["dark_mode"] avant d'instancier le widget renverrait la
# valeur de l'exécution précédente, pas le clic qui vient de se produire.
with st.sidebar:
    dark_mode = st.toggle("Light/dark mode", value=True, key="dark_mode")

t = theme.get(dark_mode)

st.markdown(f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {t['app_bg']};
        color: {t['text']};
    }}
    [data-testid="stSidebar"] {{
        background-color: {t['sidebar_bg']};
    }}
    .stApp, .stApp p, .stApp span, .stApp label {{
        color: {t['text']};
    }}
    div[data-testid="stImage"] img {{ border-radius: 12px 12px 0 0; }}
    .card {{
        border: 1px solid {t['card_border']};
        background-color: {t['card_bg']};
        border-radius: 12px; padding: 0 0 0.9rem 0;
        margin-bottom: 1rem; overflow: hidden;
    }}
    .color-block {{ height: 140px; border-radius: 12px 12px 0 0; }}
    .card-body {{ padding: 0 0.9rem; }}
    .card-title {{ font-weight: 600; margin: 0.6rem 0 0.2rem 0; display: block; color: {t['text']}; }}
    .card-meta {{ font-size: 0.8rem; color: {t['muted_text']}; margin-bottom: 0.4rem; }}
    .tag-pill {{
        display: inline-block; background: {t['pill_bg']}; color: {t['text']};
        border-radius: 999px; padding: 0.1rem 0.55rem; font-size: 0.72rem;
        margin: 0 0.25rem 0.25rem 0;
    }}
    /* Streamlit's own input/select components resolve their theme from the
       browser's prefers-color-scheme, independently of the toggle above —
       force them to follow it instead (the dropdown listbox is portaled to
       <body>, so these selectors are intentionally unscoped from .stApp). */
    body {{ background-color: {t['app_bg']}; color-scheme: {"dark" if dark_mode else "light"}; }}
    [data-testid="stTextInputRootElement"],
    [data-testid="stMultiSelectDropdown"],
    [data-testid="stMultiSelectTagsContainer"],
    [data-baseweb="select"] {{
        background-color: {t['card_bg']} !important;
        border-color: {t['card_border']} !important;
        color: {t['text']} !important;
    }}
    [data-testid="stTextInputRootElement"] input,
    [role="listbox"], [role="option"], [role="listbox"] * {{
        color: {t['text']} !important;
        background-color: transparent !important;
    }}
    /* st.pills (tag filter) renders as plain <button>s — same native-theme
       leak as the inputs above; unselected pills only, so the accent color
       marking a selected tag stays untouched. */
    [data-testid="stButtonGroup"] button[aria-checked="false"],
    [data-testid="stButtonGroup"] button:not([aria-checked]) {{
        background-color: {t['card_bg']} !important;
        color: {t['text']} !important;
        border-color: {t['card_border']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

init_db()


@st.cache_data(ttl=REFRESH_TTL_SECONDS, show_spinner="Fetching latest articles…")
def refresh_articles():
    return save_articles(fetch_all_articles())


refresh_articles()

with st.sidebar:
    search = st.text_input("Search", placeholder="Title, summary, tag, source…")
    st.divider()
    sort_label = st.radio("Sort by", ["Newest", "Most popular"])
    sort = "popularity" if sort_label == "Most popular" else "recent"
    # st.multiselect's searchable dropdown always injects an unremovable
    # "Select all" bulk action (client-side, no Python param to disable it) —
    # st.pills has no such combobox chrome and suits a small fixed tag list.
    selected_tags = st.pills("Tags", get_all_tags(), selection_mode="multi") or []

articles = get_articles(search=search, tags=selected_tags, sort=sort)

st.caption(f"{len(articles)} article(s)")

if not articles:
    st.info("No articles match your filters yet.")
else:
    cols_per_row = 4
    rows = [articles[i:i + cols_per_row] for i in range(0, len(articles), cols_per_row)]
    for row in rows:
        cols = st.columns(cols_per_row)
        for col, article in zip(cols, row):
            with col:
                with st.container(border=False):
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    if article["image"]:
                        st.image(article["image"], use_container_width=True)
                    else:
                        block_color = color_for(article["tags"], dark_mode)
                        st.markdown(f'<div class="color-block" style="background:{block_color};"></div>',
                                    unsafe_allow_html=True)

                    meta_bits = [article["source"] or "", (article["published"] or "")[:10]]
                    if article["popularity"]:
                        meta_bits.append(f"⭐ {article['popularity']}")
                    if article["extra"]:
                        meta_bits.append(article["extra"])

                    tags_html = "".join(f'<span class="tag-pill">{tag}</span>' for tag in article["tags"])

                    st.markdown(f'''
                        <div class="card-body">
                            <a class="card-title" href="{article['link']}" target="_blank">{article['title']}</a>
                            <div class="card-meta">{" · ".join(b for b in meta_bits if b)}</div>
                            {tags_html}
                        </div>
                    ''', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
