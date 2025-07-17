import streamlit as st
from ai_writer.spin_chapter import spin_chapter
from ai_writer.ai_review import ai_review
from versioning.chromadb_handler import VersionManager
from human_loop.rl_feedback import calculate_reward
from scraping.playwright_scraper import fetch_chapter, fetch_chapter_simple, fetch_chapter_playwright
import time
import fitz  # PyMuPDF
import base64

vm = VersionManager()

st.set_page_config(page_title="📚 Book Automation Agent", layout="wide")
st.title("📘 Book Automation Dashboard")

tabs = st.tabs(["📖 Spin Chapter", "🧠 AI Review", "💾 Save/Version", "📜 Version History", "✍️ Human Edit", "🎤 Voice Assistant"])

# ---------- Utility Functions ----------
def read_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def download_button(content, filename="spun_chapter.txt"):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Spun Chapter</a>'
    st.markdown(href, unsafe_allow_html=True)

# ---------- Tab 1: Spin Chapter ----------
with tabs[0]:
    st.header("Spin a Raw Chapter with LLM")

    input_type = st.selectbox("Input Type", ["📝 Paste Text", "📄 Upload File (.txt/.pdf)", "🔗 URL"], key="spin_type")
    raw_text = ""

    if input_type == "📝 Paste Text":
        raw_text = st.text_area("Paste your chapter content here:", height=300)

    elif input_type == "📄 Upload File (.txt/.pdf)":
        file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
        if file:
            if file.type == "application/pdf":
                raw_text = read_pdf(file)
            else:
                raw_text = file.read().decode("utf-8")
            st.text_area("File Content:", raw_text, height=300)

    elif input_type == "🔗 URL":
        url = st.text_input("Enter the URL:")
        scraper_method = st.selectbox("Choose scraping method:", ["🎭 Playwright", "🌐 Simple HTTP", "🔧 Auto"], key="scraper_method")

        if url and st.button("🔍 Fetch Content"):
            with st.spinner("Fetching content..."):
                try:
                    if scraper_method == "🎭 Playwright":
                        raw_text = fetch_chapter_playwright(url)
                    elif scraper_method == "🌐 Simple HTTP":
                        raw_text = fetch_chapter_simple(url)
                    else:
                        raw_text = fetch_chapter(url)

                    st.session_state["fetched_text"] = raw_text

                    if raw_text.startswith("Error:"):
                        st.error(raw_text)
                    else:
                        st.success("✅ Content fetched!")
                except Exception as e:
                    st.error(f"❌ Error fetching content: {str(e)}")
                    try:
                        raw_text = fetch_chapter_simple(url)
                        st.session_state["fetched_text"] = raw_text
                        if not raw_text.startswith("Error:"):
                            st.success("✅ Fallback method succeeded!")
                    except Exception as e2:
                        st.error(f"❌ All methods failed: {str(e2)}")

        raw_text = st.session_state.get("fetched_text", "")
        if raw_text and not raw_text.startswith("Error:"):
            st.text_area("Fetched Content:", raw_text, height=300)

    if raw_text and not raw_text.startswith("Error:") and st.button("🔁 Spin Chapter"):
        with st.spinner("Spinning chapter..."):
            try:
                spun_output = spin_chapter(raw_text)
                st.session_state["spun_chapter"] = spun_output
                st.success("✅ Chapter Spun!")
            except Exception as e:
                st.error(f"❌ Error during spinning: {e}")

    if "spun_chapter" in st.session_state:
        st.text_area("Spun Chapter Output:", st.session_state["spun_chapter"], height=300)
        download_button(st.session_state["spun_chapter"])

# ---------- Tab 2: AI Review ----------
with tabs[1]:
    st.header("AI Review of Chapter")

    input_type = st.selectbox("Review Input Type", ["📝 Paste Text", "📄 Upload File (.txt/.pdf)"], key="review_type")
    review_input = ""

    if input_type == "📝 Paste Text":
        review_input = st.text_area("Enter the text to review:", height=300)
    elif input_type == "📄 Upload File (.txt/.pdf)":
        file = st.file_uploader("Upload a file for review", type=["txt", "pdf"], key="review_file")
        if file:
            if file.type == "application/pdf":
                review_input = read_pdf(file)
            else:
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
                try:
                    vm.add_version(chapter_title, final_content, author)
                    st.success("✅ Version Saved")
                except Exception as e:
                    st.error(f"❌ Error saving version: {e}")
        else:
            st.warning("⚠️ Please fill in all fields.")

# ---------- Tab 4: Version History ----------
with tabs[3]:
    st.header("Version History")
    if st.button("🔍 Load Versions"):
        with st.spinner("Loading..."):
            try:
                versions = vm.show_all_versions()
                if versions:
                    for i, v in enumerate(versions):
                        with st.expander(f"Version {i+1}: {v.get('chapter', 'Unknown')}"):
                            st.markdown(f"**Chapter**: {v.get('chapter', 'N/A')}")
                            st.markdown(f"**Author**: {v.get('author', 'N/A')}")
                            st.markdown(f"**Timestamp**: {v.get('timestamp', 'N/A')}")
                            st.code(v.get('content', 'No content'), language='markdown')
                else:
                    st.info("📝 No versions found.")
            except Exception as e:
                st.error(f"❌ Error loading versions: {e}")

# ---------- Tab 5: Human Edit + RL ----------
with tabs[4]:
    st.header("Human Edits & Feedback")
    edited_text = st.text_area("Edit your chapter:", height=300)
    feedback_choice = st.selectbox("Was your edit better?", ["👍 Yes", "👎 No", "😐 Neutral"])
    similarity_score = st.slider("Similarity with Original", 0.0, 1.0, 0.5)
    edit_count = st.number_input("Number of edits made", min_value=0, step=1)

    if st.button("📤 Submit Feedback"):
        try:
            accepted = feedback_choice == "👍 Yes"
            reward = calculate_reward(edit_count, similarity_score, accepted)
            st.success(f"✅ Reward Score Computed: **{reward}**")
        except Exception as e:
            st.error(f"❌ Error calculating reward: {e}")

# ---------- Tab 6: Voice Assistant ----------
with tabs[5]:
    st.header("🎤 Voice Interface (Coming Soon)")
    st.info("Voice commands & TTS will be added soon.")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🔧 Debug Info")
    if st.button("🗑️ Clear Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Session cleared!")
        st.rerun()
