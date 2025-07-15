from agent_api.agent_pipeline import run_pipeline
from human_loop.editor_interface import run_editor_interface

import streamlit as st

st.title("📚 Book Rewrite Automation Agent")
url = st.text_input("Enter Chapter URL")

if st.button("Run Pipeline") and url:
    rewritten, review, version_id = run_pipeline(url)
    st.write("Review:", review)
    final = run_editor_interface("Fetched content", rewritten)
    if final:
        st.write("✅ Final submission saved with ID:", version_id)