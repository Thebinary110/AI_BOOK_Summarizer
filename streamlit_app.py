import streamlit as st
from ai_writer.spin_chapter import spin_chapter
from ai_writer.ai_review import ai_review
from versioning.chromadb_handler import VersionManager
from human_loop.rl_feedback import calculate_reward
from scraping.playwright_scraper import fetch_chapter
import time

vm = VersionManager()

st.set_page_config(page_title="📚 Book Automation Agent", layout="wide")
st.title("📘 Book Automation Dashboard")

tabs = st.tabs(["📖 Spin Chapter", "🧠 AI Review", "💾 Save/Version", "📜 Version History", "✍️ Human Edit", "🎤 Voice Assistant"])

# ---------- Tab 1: Spin Chapter ----------
with tabs[0]:
    st.header("Spin a Raw Chapter with LLM")

    input_type = st.selectbox("Input Type", ["📝 Paste Text", "📄 Upload File", "🔗 URL"], key="spin_type")

    raw_text = ""
    if input_type == "📝 Paste Text":
        raw_text = st.text_area("Paste your chapter content here:", height=300)
    elif input_type == "📄 Upload File":
        file = st.file_uploader("Upload a .txt file", type=["txt"])
        if file:
            raw_text = file.read().decode("utf-8")
            st.text_area("File Content:", raw_text, height=300)
    elif input_type == "🔗 URL":
        url = st.text_input("Enter the URL:")
        if url and st.button("🔍 Fetch Content"):
            raw_text = fetch_chapter(url)
            st.session_state["fetched_text"] = raw_text
        raw_text = st.session_state.get("fetched_text", "")
        if raw_text:
            st.text_area("Fetched Content:", raw_text, height=300)

    if raw_text and st.button("🔁 Spin Chapter"):
        with st.spinner("Spinning chapter..."):
            try:
                spun_output = spin_chapter(raw_text)
                st.session_state["spun_chapter"] = spun_output
                st.success("✅ Chapter Spun!")
            except Exception as e:
                st.error(f"❌ Error during spinning: {e}")

    if "spun_chapter" in st.session_state:
        st.text_area("Spun Chapter Output:", st.session_state["spun_chapter"], height=300)

# ---------- Tab 2: AI Review ----------
with tabs[1]:
    st.header("AI Review of Chapter")

    input_type = st.selectbox("Review Input Type", ["📝 Paste Text", "📄 Upload File"], key="review_type")

    review_input = ""
    if input_type == "📝 Paste Text":
        review_input = st.text_area("Enter the text to review:", height=300)
    elif input_type == "📄 Upload File":
        file = st.file_uploader("Upload a .txt file for review", type=["txt"], key="review_file")
        if file:
            review_input = file.read().decode("utf-8")
            st.text_area("File Content for Review:", review_input, height=300)

    if review_input and st.button("🧠 Run AI Review"):
        with st.spinner("Running AI Review..."):
            try:
                reviewed = ai_review(review_input)
                st.session_state["reviewed_output"] = reviewed
                st.success("✅ Review Complete")
            except Exception as e:
                st.error(f"❌ Error during review: {e}")

    if "reviewed_output" in st.session_state:
        st.text_area("AI Reviewed Output:", st.session_state["reviewed_output"], height=300)

# ---------- Tab 3: Save/Version ----------
with tabs[2]:
    st.header("Save a Chapter Version")
    chapter_title = st.text_input("Chapter Title")
    author = st.text_input("Author")
    final_content = st.text_area("Final Chapter Content:", height=300)
    if st.button("💾 Save Version"):
        if chapter_title and author and final_content:
            with st.spinner("Saving..."):
                vm.add_version(chapter_title, final_content, author)
                st.success("✅ Version Saved")
        else:
            st.warning("⚠️ Please fill in all fields.")

# ---------- Tab 4: Version History ----------
with tabs[3]:
    st.header("Version History")
    if st.button("🔍 Load Versions"):
        with st.spinner("Loading..."):
            versions = vm.show_all_versions()
            for v in versions:
                st.markdown(f"**Chapter**: {v['chapter']}")
                st.markdown(f"**Author**: {v['author']}")
                st.markdown(f"**Timestamp**: {v['timestamp']}")
                st.code(v['content'], language='markdown')
                st.markdown("---")

# ---------- Tab 5: Human Edit + RL ----------
with tabs[4]:
    st.header("Human Edits & Feedback")
    edited_text = st.text_area("Edit your chapter:", height=300)
    feedback_choice = st.selectbox("Was your edit better?", ["👍 Yes", "👎 No", "😐 Neutral"])
    similarity_score = st.slider("Similarity with Original", 0.0, 1.0, 0.5)
    edit_count = st.number_input("Number of edits made", min_value=0, step=1)

    if st.button("📤 Submit Feedback"):
        accepted = feedback_choice == "👍 Yes"
        reward = calculate_reward(edit_count, similarity_score, accepted)
        st.success(f"✅ Reward Score Computed: **{reward}**")

# ---------- Tab 6: Voice Assistant ----------
with tabs[5]:
    st.header("🎤 Voice Interface (Coming Soon)")
    st.info("Voice commands & TTS will be added in a future version.")

st.markdown("---")
st.markdown("🚀 Built by Shhaurya Jaiswal | Powered by Streamlit + Transformers + ChromaDB")
