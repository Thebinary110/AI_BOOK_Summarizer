import google.generativeai as genai

# Your API key (ensure it's securely stored in real projects)
genai.configure(api_key="AIzaSyAxa2W7PU9N_nAOW0wGq1tuNYaoDT5wluM")

def spin_chapter(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        author name here .
You are a creative and experienced book editor.
Rewrite the following chapter using fresh sentence structures, enhanced vocabulary, and natural flow.
Preserve the original meaning, tone, characters, and storyline.
Do not add page numbers or any metadata.
Keep the rewritten content human-readable, fluent, and logically cohesive.

### Chapter to Rewrite:
{text}

### Rewritten Chapter:
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Error during spinning: {str(e)}"
