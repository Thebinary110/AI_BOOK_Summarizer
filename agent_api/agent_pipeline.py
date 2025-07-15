from scraping.playwright_scraper import fetch_chapter
from ai_writer.spin_chapter import spin_chapter
from ai_writer.ai_review import review_text
from versioning.chromadb_handler import store_version
from agent_api.voice_interface import speak

import uuid

def run_pipeline(url):
    original = fetch_chapter(url)
    rewritten = spin_chapter(original)
    review = review_text(original, rewritten)
    version_id = str(uuid.uuid4())

    store_version(original, rewritten, {"id": version_id, "url": url, "review": review})
    speak("Rewrite complete. Review says: " + review)
    return rewritten, review, version_id

