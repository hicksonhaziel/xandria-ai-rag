#!/usr/bin/env python3
import os
import json
import hashlib
from playwright.sync_api import sync_playwright

def url_to_filename(url):
    """Convert URL to safe filename"""
    hash_part = hashlib.md5(url.encode()).hexdigest()[:8]
    safe = url.replace('https://', '').replace('http://', '')
    safe = safe.replace('/', '_').replace('?', '_').replace('&', '_')[:50]
    return f"{safe}_{hash_part}.txt"

def scrape_all():
    # Load URLs
    input_path = 'data/urls/docs/urls.json'
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return

    with open(input_path) as f:
        urls = json.load(f)
    
    os.makedirs('data/raw_contents/docs', exist_ok=True)
    
    print("Starting Playwright browser...")
    
    with sync_playwright() as p:
        # Launch Firefox
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0")
        page = context.new_page()
        
        print(f"Scraping {len(urls)} URLs...\n")
        success, failed = 0, 0
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url}")
            
            try:
                # 1. Use 'domcontentloaded' (faster/less strict)
                # 2. Increased timeout to 60s
                response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                # If the page is still loading extra JS, give it a tiny bit of extra time
                page.wait_for_timeout(2000) 
                
                if response and response.status < 400:
                    title = page.title()
                    content = page.inner_text('body')
                    
                    if content and len(content) > 100:
                        filename = url_to_filename(url)
                        filepath = f"data/raw_contents/docs/{filename}"
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"URL: {url}\n")
                            f.write(f"TITLE: {title}\n")
                            f.write("="*80 + "\n\n")
                            f.write(content)
                        
                        print(f"  ✓ Saved ({len(content)} chars)\n")
                        success += 1
                    else:
                        print(f"  ✗ Failed: Content too short\n")
                        failed += 1
                else:
                    status = response.status if response else "No Response"
                    print(f"  ✗ Failed: HTTP {status}\n")
                    failed += 1
                    
            except Exception as e:
                print(f"  ✗ Error (Timeout or Connection): {str(e)[:50]}...\n")
                failed += 1
        
        browser.close()
    
    print("="*80)
    print(f"Complete! ✓ {success} | ✗ {failed}")

if __name__ == "__main__":
    scrape_all()