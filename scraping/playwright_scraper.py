from playwright.sync_api import sync_playwright

def fetch_chapter(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        text = page.inner_text('body')
        screenshot = page.screenshot(path="chapter.png")
        browser.close()
    return text
