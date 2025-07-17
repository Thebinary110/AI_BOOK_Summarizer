import asyncio
import threading
import queue
import requests
from bs4 import BeautifulSoup
import time
import os
import sys

def fetch_chapter_simple(url):
    """Simple fallback scraper using requests and BeautifulSoup"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        return f"Error: Could not fetch content from {url}. {str(e)}"

def fetch_chapter_playwright(url, txt_path="chapter.txt", image_path="chapter.png"):
    """Playwright scraper that runs in a separate process to avoid event loop issues"""
    
    def run_playwright_process():
        """Run Playwright in a separate thread with proper Windows handling"""
        try:
            # Import Playwright here to avoid issues if not installed
            from playwright.async_api import async_playwright
            
            # Set the asyncio event loop policy for Windows
            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            
            async def fetch_async():
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page()
                    
                    try:
                        # Navigate to URL with longer timeout
                        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                        await page.wait_for_timeout(3000)

                        # Take screenshot
                        await page.screenshot(path=image_path, full_page=True)
                        print(f"Screenshot saved as {image_path}")

                        # Get text content
                        content = await page.inner_text("body")
                        
                        # Save to file
                        with open(txt_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"Text content saved as {txt_path}")

                        return content
                        
                    except Exception as e:
                        print(f"Error in Playwright navigation: {e}")
                        return f"Error: Could not fetch content from {url}. {str(e)}"
                    finally:
                        await browser.close()
            
            # Create new event loop and run
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(fetch_async())
                return result
            finally:
                loop.close()
                
        except ImportError:
            return "Error: Playwright not installed. Please install with: pip install playwright && playwright install chromium"
        except Exception as e:
            return f"Error: Playwright failed - {str(e)}"
    
    # Use threading to run Playwright
    result_queue = queue.Queue()
    
    def thread_worker():
        try:
            result = run_playwright_process()
            result_queue.put(('success', result))
        except Exception as e:
            result_queue.put(('error', f"Error: {str(e)}"))
    
    # Start thread
    thread = threading.Thread(target=thread_worker)
    thread.daemon = True
    thread.start()
    thread.join(timeout=60)  # 60 second timeout
    
    # Get result
    if not result_queue.empty():
        status, result = result_queue.get()
        return result
    else:
        return "Error: Playwright operation timed out"

def fetch_chapter(url, txt_path="chapter.txt", image_path="chapter.png"):
    """Main function that tries Playwright first, then falls back to simple scraping"""
    
    print(f"Attempting to fetch content from: {url}")
    
    # Try Playwright first
    try:
        result = fetch_chapter_playwright(url, txt_path, image_path)
        if not result.startswith("Error:"):
            print("✅ Successfully fetched with Playwright")
            return result
        else:
            print("❌ Playwright failed, trying simple method...")
    except Exception as e:
        print(f"❌ Playwright exception: {e}")
    
    # Fallback to simple scraping
    try:
        result = fetch_chapter_simple(url)
        if not result.startswith("Error:"):
            print("✅ Successfully fetched with simple method")
            # Save to file for consistency
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"Text content saved as {txt_path}")
            return result
        else:
            print("❌ Simple method also failed")
            return result
    except Exception as e:
        return f"Error: Both scraping methods failed. {str(e)}"

# For backward compatibility
def fetch_chapter_legacy(url, txt_path="chapter.txt", image_path="chapter.png"):
    """Legacy function name"""
    return fetch_chapter(url, txt_path, image_path)