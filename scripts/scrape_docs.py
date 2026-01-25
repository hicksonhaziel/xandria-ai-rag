#!/usr/bin/env python3
"""
Scrape Xandeum documentation and upload to Pinecone
"""

import os
import requests
from bs4 import BeautifulSoup
from pinecone import Pinecone
from dotenv import load_dotenv
from helpers import (
    generate_embedding,
    chunk_text,
    generate_id,
    clean_text,
    rate_limit_sleep,
    log_progress,
    save_progress,
    load_progress
)

# Load environment
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index('xandria-knowledge')


def scrape_page(url: str) -> dict:
    """
    Scrape a single documentation page
    
    Args:
        url: URL to scrape
        
    Returns:
        Dict with page data or None if failed
    """
    try:
        log_progress(f"Scraping: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Extract title
        title = soup.find('h1')
        title = title.get_text().strip() if title else soup.find('title').get_text().strip()
        
        # Extract main content
        # Try different common content containers
        content = None
        for selector in ['main', 'article', '.content', '.documentation', '#content']:
            content = soup.select_one(selector)
            if content:
                break
        
        # Fallback to body if no content container found
        if not content:
            content = soup.find('body')
        
        text = content.get_text() if content else ""
        text = clean_text(text)
        
        return {
            'url': url,
            'title': title,
            'content': text,
            'scraped_at': None  # Will be set when uploading
        }
        
    except Exception as e:
        log_progress(f"Failed to scrape {url}: {e}", "ERROR")
        return None


def process_and_upload(page_data: dict, namespace: str = 'xandeum-docs'):
    """
    Process page content and upload to Pinecone
    
    Args:
        page_data: Page data from scrape_page()
        namespace: Pinecone namespace to use
    """
    log_progress(f"Processing: {page_data['title']}")
    
    # Split into chunks
    chunks = chunk_text(page_data['content'], chunk_size=500, overlap=50)
    log_progress(f"  Created {len(chunks)} chunks")
    
    # Process each chunk
    vectors = []
    
    for i, chunk in enumerate(chunks):
        log_progress(f"  Processing chunk {i+1}/{len(chunks)}")
        
        # Generate embedding
        rate_limit_sleep(1.0)  # Rate limiting for FREE tier
        embedding = generate_embedding(chunk)
        
        # Create vector
        vector_id = generate_id('doc_xandeum', i)
        
        vectors.append({
            'id': vector_id,
            'values': embedding,
            'metadata': {
                'text': chunk[:1000],  # Limit metadata size
                'source': 'xandeum_docs',
                'url': page_data['url'],
                'title': page_data['title'],
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
        })
    
    # Upload to Pinecone in batches
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)
        log_progress(f"  Uploaded batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1}")
    
    log_progress(f"✓ Completed: {page_data['title']}")
    return len(vectors)


def scrape_all_docs(urls: list):
    """
    Scrape all documentation pages
    
    Args:
        urls: List of URLs to scrape
    """
    log_progress("=" * 60)
    log_progress("Starting Xandeum Documentation Scraping")
    log_progress("=" * 60)
    
    # Load progress if exists
    progress = load_progress('scrape_docs_progress.json')
    completed_urls = progress.get('completed_urls', [])
    
    total_vectors = 0
    successful = 0
    failed = 0
    
    for idx, url in enumerate(urls):
        log_progress(f"\nPage {idx+1}/{len(urls)}")
        
        # Skip if already processed
        if url in completed_urls:
            log_progress(f"Skipping (already processed): {url}")
            continue
        
        # Scrape page
        page_data = scrape_page(url)
        
        if page_data:
            # Process and upload
            try:
                vectors_count = process_and_upload(page_data)
                total_vectors += vectors_count
                successful += 1
                
                # Save progress
                completed_urls.append(url)
                save_progress('scrape_docs_progress.json', {
                    'completed_urls': completed_urls,
                    'total_vectors': total_vectors,
                    'successful': successful,
                    'failed': failed
                })
                
            except Exception as e:
                log_progress(f"Failed to process {url}: {e}", "ERROR")
                failed += 1
        else:
            failed += 1
        
        # Wait between pages
        rate_limit_sleep(2.0)
    
    # Final summary
    log_progress("\n" + "=" * 60)
    log_progress("Scraping Complete!")
    log_progress("=" * 60)
    log_progress(f"Successful: {successful}")
    log_progress(f"Failed: {failed}")
    log_progress(f"Total vectors uploaded: {total_vectors}")
    log_progress(f"💰 Cost: $0.00 (FREE!)")


def main():
    """Main function"""
    
    # List of Xandeum documentation URLs to scrape
    # TODO: Replace with actual Xandeum docs URLs
    urls = [
        'https://docs.xandeum.com/',
        'https://docs.xandeum.com/getting-started',
        'https://docs.xandeum.com/installation',
        # Add more URLs here
    ]
    
    log_progress(f"Found {len(urls)} URLs to scrape")
    log_progress("Starting in 3 seconds... (Press Ctrl+C to cancel)")
    
    import time
    time.sleep(3)
    
    scrape_all_docs(urls)


if __name__ == "__main__":
    main()