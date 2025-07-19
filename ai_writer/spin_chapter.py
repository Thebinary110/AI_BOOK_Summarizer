import google.generativeai as genai

# Your API key (ensure it's securely stored in real projects)
genai.configure(api_key="AIzaSyC1vhpAPdh50lHUZYyx_dWq7quMpzPw_h0")

def spin_chapter(text, chapter_title="Untitled Chapter", author_name="Unknown Author"):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Chapter Title: {chapter_title}
Author: {author_name}

As a skilled book editor, your job is to rewrite the following chapter to improve its sentence flow, vocabulary, and readability, without altering the story, tone, or meaning.

Keep your output:
- Human-readable
- Clear and logically structured
- Faithful to the original characters and themes

Do not include any metadata or commentary. Just return the rewritten chapter with the following heading:

---
Chapter Title: {chapter_title}
Author: {author_name}
---

Chapter:
{text}

Please rewrite the chapter now:
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error during spinning: {str(e)}"
