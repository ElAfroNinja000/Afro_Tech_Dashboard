import streamlit as st
from feeds import fetch_articles
from db import init_db, save_articles, get_articles_by_topic

st.set_page_config(page_title="Veille Tech", layout="wide")

init_db()
if st.button("🔄 Refresh Feeds"):
    new_articles = fetch_articles()
    save_articles(new_articles)
    st.success("Update Complete!")

# Affichage des articles
grouped = get_articles_by_topic()
st.title("🍀 Creative Development Portal 🚀")

if grouped:
    cols = st.columns(len(grouped))
    for idx, (topic, articles) in enumerate(grouped.items()):
        with cols[idx]:

            for idx, (topic, articles) in enumerate(grouped.items()):
                with cols[idx]:
                    st.markdown(f"### 🎨 {topic}")
                    for topic, title, link, published, image in articles:
                        with st.container(border=True):
                            if image:
                                st.image(image, use_container_width=True)
                            st.markdown(f"**[{title}]({link})**", unsafe_allow_html=True)
                            st.markdown(f"<small>{published}</small>", unsafe_allow_html=True)
                            st.markdown("""
                                <style>
                                div[data-testid="stImage"] img {
                                    border-radius: 12px;
                                }
                                .element-container {
                                    padding-bottom: 1rem;
                                }
                                </style>
                            """, unsafe_allow_html=True)

