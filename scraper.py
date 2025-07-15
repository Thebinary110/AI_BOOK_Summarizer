from playwright.sync_api import sync_playwright
import os

def scrape_chapter(url, txt_path="chapter.txt", image_path="chapter.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)

        # take screenshot
        page.screenshot(path=image_path, full_page=True)
        print(f"screenshot saved as {image_path}")

        # get text content
        content = page.inner_text("body")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"text content saved as {txt_path}")

        browser.close()

if __name__ == "__main__":
    test_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    scrape_chapter(test_url)
