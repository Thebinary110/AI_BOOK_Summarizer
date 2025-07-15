def review_text(original: str, rewritten: str) -> str:
    if original[:30].lower() in rewritten.lower():
        return "❌ Possible copy-paste detected."
    if len(rewritten) < len(original) * 0.5:
        return "⚠️ Too short."
    return "✅ Review passed."

