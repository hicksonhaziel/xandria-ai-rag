#!/usr/bin/env python3
import requests, json, os, re
from bs4 import BeautifulSoup

def get_channel_videos(channel_url):
    """Scrape YouTube channel for video links and titles"""
    r = requests.get(channel_url)
    
    # Extract video data from page script
    video_pattern = r'"videoId":"([^"]+)".*?"title":{"runs":\[{"text":"([^"]+)"'
    matches = re.findall(video_pattern, r.text)
    
    videos = []
    seen = set()
    
    for video_id, title in matches:
        if video_id not in seen:
            seen.add(video_id)
            videos.append({
                "link": f"https://youtu.be/{video_id}",
                "title": title,
                "channel": "BlockchainBernie"
            })
    
    return videos

def filter_xandeum_videos(videos):
    """Filter only Xandeum-related videos"""
    keywords = ['xandeum', 'pnode', 'xand', 'solana storage', 'decentralized storage']
    
    filtered = []
    for video in videos:
        title_lower = video['title'].lower()
        if any(kw in title_lower for kw in keywords):
            filtered.append(video)
            print(f"  ✓ {video['title']}")
        else:
            print(f"  ✗ {video['title']}")
    
    return filtered

def main():
    channel_url = "https://www.youtube.com/@BlockchainBernie/videos"
    
    print("Fetching videos from BlockchainBernie...\n")
    videos = get_channel_videos(channel_url)
    
    print(f"\nFound {len(videos)} total videos")
    print("\nFiltering for Xandeum content...\n")
    
    xandeum_videos = filter_xandeum_videos(videos)
    
    # Load existing if present
    os.makedirs('data', exist_ok=True)
    existing = []
    if os.path.exists('data/youtube_urls.json'):
        with open('data/youtube_urls.json') as f:
            existing = json.load(f)
    
    # Combine
    all_videos = existing + xandeum_videos
    
    # Save
    with open('data/youtube_urls.json', 'w') as f:
        json.dump(all_videos, f, indent=4)
    
    print(f"\n✅ Found {len(xandeum_videos)} Xandeum videos")
    print(f"Total with existing: {len(all_videos)}")
    print("Saved to: data/youtube_urls.json")

if __name__ == "__main__":
    main()