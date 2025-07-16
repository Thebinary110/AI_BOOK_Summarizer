from transformers import pipeline

def ai_review(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Truncate text if it exceeds the model limit
    max_input_chars = 1024  # safe number for BART
    if len(text) > max_input_chars:
        text = text[:max_input_chars]

    result = summarizer(text, max_length=300, min_length=30, do_sample=False)
    reviewed_output = result[0]['summary_text']
    return reviewed_output
