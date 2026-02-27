import streamlit as st
from search import web_search
from extract import fetch_and_extract
from agent import generate_report

st.set_page_config(page_title="A3 Web Research Agent", page_icon="🔎")

st.title("🔎 A3 — Agent de Recherche Web")
st.caption("Question → Web → Extraction → Synthèse citée")

question = st.text_input("Question", placeholder="Ex : Quelles sont les tendances IA en 2025 ?")
sources_count = st.slider("Nombre de sources", 3, 8, 5)

if st.button("Générer", type="primary") and question:
    with st.spinner("Recherche web..."):
        results = web_search(question, sources_count)

    docs = []
    with st.spinner("Extraction des pages..."):
        for r in results:
            docs.append({
                "title": r["title"],
                "url": r["href"],
                "text": fetch_and_extract(r["href"])
            })

    st.subheader("Rapport")
    report = generate_report(question, docs)
    st.write(report)

