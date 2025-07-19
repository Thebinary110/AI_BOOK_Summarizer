import google.generativeai as genai

genai.configure(api_key="AIzaSyAxa2W7PU9N_nAOW0wGq1tuNYaoDT5wluM")

def ai_review(text, book_title="Unknown Book", chapter_name="Unknown Chapter", author_name="Unknown Author"):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are a seasoned literary critic. Given the following book chapter, write a concise and thoughtful review (not a summary) that highlights the tone, themes, and style in 5–7 lines.

Start with:
Book Title : {book_title}
Chapter    : {chapter_name}
Author     : {author_name}

Then write:
Chapter Review:
"""

        response = model.generate_content(prompt + "\n\n" + text)
        return response.text.strip()

    except Exception as e:
        return f"Error in review generation: {str(e)}"
