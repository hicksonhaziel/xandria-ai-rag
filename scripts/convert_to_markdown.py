#!/usr/bin/env python3
"""
Xandria AI Ingestion - Raw Content to Clean Markdown Converter
Uses Groq API (Llama 3.3 70B) to clean and structure raw docs, videos, discord chats
"""

import os
import re
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import tiktoken

# Load environment variables
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_DIR = Path("data/raw_contents")
OUTPUT_DIR = Path("data/clean_markdown")
PROGRESS_FILE = Path("data/conversion_progress.json")

# Rate limiting: 1 file per minute to avoid 429 errors
DELAY_SECONDS = 30
MAX_TOKENS_PER_REQUEST = 6000  # Split files larger than this

# Folder mapping: raw folder -> clean output folder
FOLDER_MAPPING = {
    "docs": "official_docs",
    "youtube_videos": "video_transcripts",
    "github_docs": "github_repos",
    "discord_troubleshoots": "discord_archives"
}

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Token counter (using tiktoken for accurate counting)
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Close enough for token estimation


def count_tokens(text: str) -> int:
    """Count tokens in text"""
    return len(encoding.encode(text))


def load_progress():
    """Load conversion progress from file"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed": [], "failed": []}


def save_progress(progress):
    """Save conversion progress"""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def extract_metadata(raw_content: str, filename: str) -> dict:
    """Extract metadata from raw content"""
    metadata = {
        "original_filename": filename,
        "source": None,
        "category": None,
        "ingested_at": time.strftime("%Y-%m-%d")
    }
    
    # Extract source URL if present
    source_match = re.search(r'source=\[(https?://[^\]]+)\]', raw_content)
    if source_match:
        metadata["source"] = source_match.group(1)
    
    # Try to extract URL from content
    url_match = re.search(r'(https?://[^\s]+)', raw_content[:500])
    if url_match and not metadata["source"]:
        metadata["source"] = url_match.group(1)
    
    return metadata


def create_cleaning_prompt(content: str, content_type: str) -> str:
    """
    THE ULTIMATE CLAUDE PROMPT - Customized for each content type
    This tells Groq's AI exactly how to clean the content
    """
    
    base_instructions = """You are a technical content editor specializing in blockchain documentation.

Your task is to convert raw, messy text into clean, professional Markdown documentation.

CRITICAL RULES:
1. Remove ALL navigation elements (sidebars, headers, footers, "Subscribe", social media links)
2. Remove repetitive elements and boilerplate text
3. Keep ONLY substantive technical content
4. Preserve all code blocks with proper language tags (```bash, ```python, ```javascript, etc.)
5. Preserve all technical commands, URLs, and configuration examples EXACTLY as written
6. For lists and steps, use proper Markdown formatting
7. Add section headers (##) to organize content logically
8. DO NOT add your own commentary or explanations - only clean what exists

"""
    
    if content_type == "youtube":
        specific_instructions = """
YOUTUBE TRANSCRIPT SPECIFIC RULES:
- Convert "00:01:23 Hey guys" format into clean prose paragraphs
- Keep timestamp references every 2-3 paragraphs for context: `[Timestamp: 12:34]`
- Remove filler words ("um", "uh", "you know", "like")
- Group related topics into sections with ## headers
- Preserve technical terms and project names exactly as spoken
- If multiple speakers, note speaker changes with **Speaker Name:**
"""
    
    elif content_type == "discord":
        specific_instructions = """
DISCORD CHAT SPECIFIC RULES:
- Group messages by topic/problem into coherent sections
- Format as: ## Problem: [brief description] followed by solution/discussion
- Preserve usernames for attribution: **@username:**
- Keep timestamps only for the first message of each topic section
- Remove bot commands, emoji spam, and off-topic chatter
- Preserve code snippets shared in chat with proper Markdown code blocks
- Summarize long back-and-forth into clear Q&A or solution steps
"""
    
    elif content_type == "github":
        specific_instructions = """
GITHUB DOCUMENTATION SPECIFIC RULES:
- Keep the README structure (# Title, ## Installation, ## Usage, etc.)
- Preserve all code examples with accurate language tags
- Keep badges and shields at the top if present
- Preserve directory trees and file structure examples
- Keep API reference tables intact
- Remove GitHub UI elements ("Star this repo", navigation breadcrumbs)
"""
    
    else:  # docs/website content
        specific_instructions = """
WEBSITE DOCUMENTATION SPECIFIC RULES:
- Remove website navigation (Home, About, Contact, etc.)
- Remove cookie notices, login prompts, subscription CTAs
- Keep technical content organized by ## headers
- Preserve configuration examples, command-line instructions
- Keep warning/info boxes but format as blockquotes (>)
- Remove "Last updated" timestamps unless part of version info
- Preserve tables and structured data
"""
    
    return f"""{base_instructions}

{specific_instructions}

Now clean this content and output ONLY the cleaned Markdown with no preamble:

{content}"""


def determine_content_type(folder_name: str, filename: str) -> str:
    """Determine what type of content this is"""
    if "youtube" in folder_name.lower():
        return "youtube"
    elif "discord" in folder_name.lower():
        return "discord"
    elif "github" in folder_name.lower():
        return "github"
    else:
        return "docs"


def generate_clean_filename(original_filename: str, content_type: str) -> str:
    """
    Generate SEO-friendly, descriptive filename
    Example: devnet.xandeum.network_validator-installation_4a951223.txt 
    -> xandeum-validator-installation.md
    """
    # Remove hash and extension
    name = re.sub(r'_[a-f0-9]{8}\.txt$', '', original_filename)
    
    # Remove domain prefixes
    name = re.sub(r'^(www\.|docs\.|devnet\.|forum\.|help\.)xandeum\.network_', '', name)
    name = re.sub(r'^xandeum\.network_', '', name)
    
    # Remove special prefixes
    name = re.sub(r'^(post_|blog_tags_|blog_categories_|t_|u_|c_)', '', name)
    
    # Replace underscores with hyphens
    name = name.replace('_', '-')
    
    # Clean up multiple hyphens
    name = re.sub(r'-+', '-', name)
    
    # Ensure it ends with .md
    if not name.endswith('.md'):
        name = name + '.md'
    
    return name.lower()


def split_content_if_needed(content: str, max_tokens: int) -> list:
    """Split content into chunks if it exceeds token limit"""
    tokens = count_tokens(content)
    
    if tokens <= max_tokens:
        return [content]
    
    # Split by paragraphs
    paragraphs = content.split('\n\n')
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for para in paragraphs:
        para_tokens = count_tokens(para)
        
        if current_tokens + para_tokens > max_tokens:
            # Save current chunk
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_tokens = para_tokens
        else:
            current_chunk.append(para)
            current_tokens += para_tokens
    
    # Add last chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def clean_content_with_groq(content: str, content_type: str) -> str:
    """Send content to Groq API for cleaning"""
    prompt = create_cleaning_prompt(content, content_type)
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical documentation editor. Output clean Markdown only, no explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for consistency
            max_tokens=8000,
        )
        
        return completion.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"  ❌ Groq API Error: {str(e)}")
        return None


def create_markdown_with_frontmatter(cleaned_content: str, metadata: dict) -> str:
    """Create final Markdown file with YAML frontmatter"""
    frontmatter = "---\n"
    
    for key, value in metadata.items():
        if value:
            frontmatter += f"{key}: {value}\n"
    
    frontmatter += "---\n\n"
    
    return frontmatter + cleaned_content


def process_file(input_path: Path, output_folder: Path, content_type: str) -> bool:
    """Process a single file: read, clean, save"""
    
    print(f"\n📄 Processing: {input_path.name}")
    
    # Read raw content
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"  ❌ Failed to read file: {e}")
        return False
    
    # Extract metadata
    metadata = extract_metadata(raw_content, input_path.name)
    
    # Check if content needs splitting
    chunks = split_content_if_needed(raw_content, MAX_TOKENS_PER_REQUEST)
    
    if len(chunks) > 1:
        print(f"  📊 File too large! Splitting into {len(chunks)} parts")
    
    # Process each chunk
    all_cleaned_parts = []
    
    for idx, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"  🔄 Cleaning part {idx}/{len(chunks)}...")
        else:
            print(f"  🔄 Cleaning content...")
        
        cleaned = clean_content_with_groq(chunk, content_type)
        
        if not cleaned:
            return False
        
        all_cleaned_parts.append(cleaned)
        
        # Rate limiting between chunks (if multiple parts)
        if idx < len(chunks):
            time.sleep(30)  # 30 seconds between chunks of same file
    
    # Combine all parts
    final_content = "\n\n---\n\n".join(all_cleaned_parts)
    
    # Create output filename
    output_filename = generate_clean_filename(input_path.name, content_type)
    output_path = output_folder / output_filename
    
    # If we had multiple parts, note it in metadata
    if len(chunks) > 1:
        metadata["parts"] = len(chunks)
        metadata["note"] = "Large file - split into multiple sections"
    
    # Create final Markdown with frontmatter
    final_markdown = create_markdown_with_frontmatter(final_content, metadata)
    
    # Save to file
    output_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)
        print(f"  ✅ Saved to: {output_path}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to save: {e}")
        return False


def main():
    """Main conversion loop"""
    
    print("🚀 Xandria AI Ingestion - Markdown Converter")
    print(f"📁 Input: {BASE_DIR}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"⏱️  Rate: 1 file per {DELAY_SECONDS} seconds\n")
    
    # Load progress
    progress = load_progress()
    
    # Collect all files to process
    all_files = []
    
    for raw_folder, clean_folder in FOLDER_MAPPING.items():
        folder_path = BASE_DIR / raw_folder
        
        if not folder_path.exists():
            print(f"⚠️  Skipping {raw_folder} (folder not found)")
            continue
        
        output_folder = OUTPUT_DIR / clean_folder
        content_type = determine_content_type(raw_folder, "")
        
        for file_path in sorted(folder_path.glob("*.txt")):
            if str(file_path) not in progress["completed"]:
                all_files.append((file_path, output_folder, content_type))
    
    if not all_files:
        print("✨ All files already processed!")
        return
    
    print(f"📊 Found {len(all_files)} files to process")
    print(f"⏰ Estimated time: {len(all_files)} minutes\n")
    
    start_time = time.time()
    
    for idx, (file_path, output_folder, content_type) in enumerate(all_files, 1):
        print(f"\n{'='*60}")
        print(f"Progress: {idx}/{len(all_files)}")
        
        success = process_file(file_path, output_folder, content_type)
        
        if success:
            progress["completed"].append(str(file_path))
        else:
            progress["failed"].append(str(file_path))
        
        # Save progress after each file
        save_progress(progress)
        
        # Rate limiting: Wait 60 seconds before next file
        if idx < len(all_files):
            print(f"\n⏳ Waiting {DELAY_SECONDS} seconds (rate limit protection)...")
            time.sleep(DELAY_SECONDS)
    
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✅ Conversion complete!")
    print(f"📊 Processed: {len(progress['completed'])} files")
    print(f"❌ Failed: {len(progress['failed'])} files")
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    
    if progress["failed"]:
        print("\n⚠️  Failed files:")
        for failed in progress["failed"]:
            print(f"  - {failed}")


if __name__ == "__main__":
    main()