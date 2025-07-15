import streamlit as st

st.set_page_config(page_title="AI Writer Editor", layout="wide")

st.title("📝 AI-Powered Book Editor")

if "content" not in st.session_state:
    st.session_state.content = ""

uploaded_file = st.file_uploader("Upload a chapter (.txt file)", type="txt")

if uploaded_file:
    st.session_state.content = uploaded_file.read().decode("utf-8")

if st.session_state.content:
    edited_text = st.text_area("✍️ Edit the paraphrased content", value=st.session_state.content, height=600)
    save_button = st.button("💾 Save")

    if save_button:
        with open("human_loop/edited_chapter.txt", "w", encoding="utf-8") as f:
            f.write(edited_text)
        st.success("Edited content saved!")
