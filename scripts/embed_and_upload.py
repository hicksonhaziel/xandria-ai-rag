#!/usr/bin/env python3
"""
Xandria AI - Smart Markdown Chunking + Embedding + Pinecone Upload
Uses Google AI Studio API (much simpler than Vertex AI!)
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import tiktoken
import hashlib
import time

# Load environment
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "xandria-knowledge-base")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CLEAN_MD_DIR = Path("data/clean_markdown")
BATCH_SIZE = 100  # Upload to Pinecone in batches
MAX_CHUNK_TOKENS = 1500  # Leave room for overlap
OVERLAP_TOKENS = 150  # Context overlap between chunks

# Initialize Google AI
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize tokenizer
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def count_tokens(text: str) -> int:
    """Count tokens in text"""
    return len(encoding.encode(text))


def extract_frontmatter(content: str) -> tuple[Dict, str]:
    """Extract YAML frontmatter and return metadata + clean content"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()
            
            # Parse YAML-like frontmatter
            metadata = {}
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
            
            return metadata, body
    
    return {}, content


def smart_chunk_markdown(content: str, metadata: Dict, max_tokens: int = MAX_CHUNK_TOKENS) -> List[Dict]:
    """
    Intelligently chunk markdown preserving context
    
    Strategy:
    1. Split by ## headers (sections)
    2. Keep code blocks intact
    3. Group Discord Q&A threads together
    4. Add overlap between chunks
    5. Preserve metadata in each chunk
    """
    chunks = []
    
    # Split by major sections (## headers)
    sections = re.split(r'\n(##\s+.+)\n', content)
    
    current_chunk = ""
    current_section_title = metadata.get("original_filename", "Unknown")
    
    for i, section in enumerate(sections):
        # Check if this is a header
        if section.startswith("##"):
            # If current chunk exists and is getting too big, save it
            if current_chunk and count_tokens(current_chunk) > max_tokens:
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": {
                        **metadata,
                        "section": current_section_title,
                        "chunk_index": len(chunks),
                        "content_type": detect_content_type(current_chunk)
                    }
                })
                
                # Start new chunk with overlap (last paragraph of previous chunk)
                overlap = get_last_paragraph(current_chunk, OVERLAP_TOKENS)
                current_chunk = overlap + "\n\n" + section
            else:
                current_chunk += "\n" + section
            
            current_section_title = section.strip()
        
        else:
            # Regular content
            current_chunk += "\n" + section
            
            # If chunk is too large, split it
            if count_tokens(current_chunk) > max_tokens:
                # Find natural break point (paragraph, code block end)
                break_point = find_break_point(current_chunk, max_tokens)
                
                if break_point > 0:
                    chunk_text = current_chunk[:break_point].strip()
                    chunks.append({
                        "text": chunk_text,
                        "metadata": {
                            **metadata,
                            "section": current_section_title,
                            "chunk_index": len(chunks),
                            "content_type": detect_content_type(chunk_text)
                        }
                    })
                    
                    # Continue with remainder + overlap
                    overlap = get_last_paragraph(chunk_text, OVERLAP_TOKENS)
                    current_chunk = overlap + "\n\n" + current_chunk[break_point:]
    
    # Add final chunk
    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "metadata": {
                **metadata,
                "section": current_section_title,
                "chunk_index": len(chunks),
                "content_type": detect_content_type(current_chunk)
            }
        })
    
    return chunks


def detect_content_type(text: str) -> str:
    """Detect what type of content this is"""
    if "```" in text:
        return "code_heavy"
    elif re.search(r'\*\*@\w+:', text):
        return "discord_chat"
    elif re.search(r'##\s+(Problem|Solution|Question)', text, re.IGNORECASE):
        return "troubleshooting"
    elif re.search(r'```(bash|python|javascript)', text):
        return "tutorial"
    else:
        return "documentation"


def find_break_point(text: str, max_tokens: int) -> int:
    """Find natural break point in text (paragraph boundary)"""
    target_pos = int(len(text) * (max_tokens / count_tokens(text)))
    
    # Look for paragraph break near target
    search_window = text[max(0, target_pos-200):min(len(text), target_pos+200)]
    
    # Try to break at double newline
    break_at = search_window.find("\n\n")
    if break_at != -1:
        return target_pos - 200 + break_at
    
    # Fallback: break at single newline
    break_at = search_window.find("\n")
    if break_at != -1:
        return target_pos - 200 + break_at
    
    return target_pos


def get_last_paragraph(text: str, max_tokens: int) -> str:
    """Get last paragraph for overlap context"""
    paragraphs = text.split("\n\n")
    overlap = ""
    
    for para in reversed(paragraphs):
        if count_tokens(overlap + para) <= max_tokens:
            overlap = para + "\n\n" + overlap
        else:
            break
    
    return overlap.strip()


def generate_embedding(text: str) -> List[float]:
    """Generate embedding using Google AI Studio API"""
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    except Exception as e:
        print(f"  ❌ Embedding failed: {e}")
        return None


def create_chunk_id(file_path: str, chunk_index: int) -> str:
    """Create unique ID for chunk"""
    hash_input = f"{file_path}_{chunk_index}"
    return hashlib.md5(hash_input.encode()).hexdigest()


def process_file(file_path: Path, category: str) -> List[Dict]:
    """Process a single markdown file into chunks with embeddings"""
    print(f"📄 Processing: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Failed to read: {e}")
        return []
    
    # Extract frontmatter metadata
    metadata, body = extract_frontmatter(content)
    metadata["category"] = category
    metadata["file_path"] = str(file_path)
    
    # Chunk the content
    chunks = smart_chunk_markdown(body, metadata)
    print(f"  📊 Created {len(chunks)} chunks")
    
    # Generate embeddings for each chunk
    embedded_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"  🔄 Embedding chunk {i+1}/{len(chunks)}...", end="\r")
        
        embedding = generate_embedding(chunk["text"])
        if embedding:
            embedded_chunks.append({
                "id": create_chunk_id(str(file_path), i),
                "values": embedding,
                "metadata": {
                    **chunk["metadata"],
                    "text": chunk["text"][:1000],  # First 1000 chars for preview
                    "full_text": chunk["text"],  # Full text for retrieval
                    "token_count": count_tokens(chunk["text"])
                }
            })
        
        # Rate limiting - Google AI Studio free tier: 1500 req/min
        time.sleep(0.1)  # 10 req/sec = 600/min (safe buffer)
    
    print(f"  ✅ Embedded {len(embedded_chunks)} chunks                    ")
    return embedded_chunks


def upload_to_pinecone(vectors: List[Dict], index):
    """Upload vectors to Pinecone in batches"""
    total = len(vectors)
    
    for i in range(0, total, BATCH_SIZE):
        batch = vectors[i:i+BATCH_SIZE]
        try:
            index.upsert(vectors=batch)
            print(f"  📤 Uploaded batch {i//BATCH_SIZE + 1} ({len(batch)} vectors)")
        except Exception as e:
            print(f"  ❌ Upload failed: {e}")


def main():
    """Main processing loop"""
    print("🚀 Xandria AI - Embedding & Pinecone Upload")
    print(f"📁 Source: {CLEAN_MD_DIR}")
    print(f"🎯 Target: Pinecone index '{PINECONE_INDEX_NAME}'\n")
    
    # Initialize Pinecone
    print("🔗 Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists, create if not
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"📦 Creating new index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,  # Google text-embedding-004 dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("⏳ Waiting for index to be ready...")
        time.sleep(10)  # Wait for index initialization
    
    index = pc.Index(PINECONE_INDEX_NAME)
    print(f"✅ Connected to index: {PINECONE_INDEX_NAME}\n")
    
    # Process all markdown files
    all_vectors = []
    total_files = 0
    total_chunks = 0
    
    for category_folder in CLEAN_MD_DIR.iterdir():
        if not category_folder.is_dir():
            continue
        
        category = category_folder.name
        print(f"\n{'='*60}")
        print(f"📂 Processing category: {category}")
        print(f"{'='*60}")
        
        md_files = list(category_folder.glob("*.md"))
        print(f"Found {len(md_files)} files\n")
        
        for md_file in md_files:
            vectors = process_file(md_file, category)
            all_vectors.extend(vectors)
            total_files += 1
            total_chunks += len(vectors)
            
            # Upload in batches to avoid memory issues
            if len(all_vectors) >= BATCH_SIZE * 5:
                print(f"\n📤 Uploading batch to Pinecone...")
                upload_to_pinecone(all_vectors, index)
                all_vectors = []
    
    # Upload remaining vectors
    if all_vectors:
        print(f"\n📤 Uploading final batch to Pinecone...")
        upload_to_pinecone(all_vectors, index)
    
    # Show final stats
    print(f"\n{'='*60}")
    print(f"✅ Processing Complete!")
    print(f"📊 Files processed: {total_files}")
    print(f"📦 Total chunks created: {total_chunks}")
    print(f"\n🔍 Querying Pinecone stats...")
    
    stats = index.describe_index_stats()
    print(f"💾 Vectors in index: {stats.total_vector_count}")
    print(f"📐 Dimensions: {stats.dimension}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()