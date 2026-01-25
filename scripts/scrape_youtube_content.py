#!/usr/bin/env python3
import os
import json
import hashlib
import re
import subprocess
import random
import time  # Added for rate limiting


def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def url_to_filename(url, title):
    hash_part = hashlib.md5(url.encode()).hexdigest()[:8]
    safe_title = "".join([c if c.isalnum() else "_" for c in title])[:50]
    return f"{safe_title}_{hash_part}.txt"

def scrape_youtube():
    input_path = 'data/urls/youtube_videos/youtube_urls.json'
    output_dir = 'data/raw_contents/youtube_videos'
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return

    with open(input_path, 'r') as f:
        videos = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    total_videos = len(videos)
    print(f"Processing {total_videos} videos at a rate of 10 per minute...")
    success, failed = 0, 0
    
    for i, video in enumerate(videos, 1):
        url = video.get('link')
        title = video.get('title', 'Unknown Title')
        video_id = extract_video_id(url)
        
        if not video_id:
            continue
            
        print(f"[{i}/{total_videos}] Processing: {title}")
        
        try:
            cmd = ["python3", "-m", "youtube_transcript_api", video_id, "--format", "text"]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0 and len(result.stdout.strip()) > 10:
                content = result.stdout.strip()
                content = " ".join(content.split())
                
                filename = url_to_filename(url, title)
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\nTITLE: {title}\n")
                    f.write("="*80 + "\n\n")
                    f.write(content)
                
                print(f"  ✓ Saved ({len(content)} chars)")
                success += 1
            else:
                # Handle cases where subtitles might be disabled
                print(f"  ✗ Failed: No transcript available or access denied.")
                failed += 1
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
            
        # Rate Limiting Logic: 
        # Wait 6 seconds before the next request, except for the very last one.
        if i < total_videos:
            print(f"  ...Waiting 6 seconds to maintain rate limit...")
            time.sleep(random.uniform(30, 60))
            
    print("-" * 30)
    print(f"Complete! ✓ {success} | ✗ {failed}")

if __name__ == "__main__":
    scrape_youtube()