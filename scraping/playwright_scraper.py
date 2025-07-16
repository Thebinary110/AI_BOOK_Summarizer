import subprocess

def fetch_chapter(url):
    # Use curl or requests as fallback since Playwright subprocess fails
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"[ERROR] Could not fetch URL: {e}"
