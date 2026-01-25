#!/usr/bin/env python3
"""
Hybrid Search: Filename Context + Vector Search + Reranking
Gives AI maximum context by combining multiple retrieval strategies
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
import cohere
from dotenv import load_dotenv
from pinecone import Pinecone
import google.generativeai as genai

load_dotenv()

# Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "xandria-knowledge-base")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CLEAN_MD_DIR = Path("data/clean_markdown")

# Initialize
genai.configure(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
co = cohere.Client(COHERE_API_KEY)


def extract_keywords(query: str) -> List[str]:
    """
    Extract meaningful keywords from query for filename matching
    Removes common words and keeps technical terms
    """
    # Common words to ignore
    stop_words = {
        'how', 'what', 'when', 'where', 'why', 'does', 'is', 'are', 'the', 
        'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'do', 'i', 'my', 'me', 'work', 'can', 'get', 'make', 'use'
    }
    
    # Clean and split query
    words = re.findall(r'\b\w+\b', query.lower())
    
    # Keep meaningful keywords
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords


def find_relevant_files_by_name(keywords: List[str]) -> Dict[str, List[Path]]:
    """
    Search through all markdown files and find those with matching filenames
    Returns dict: {category: [matching_files]}
    """
    relevant_files = {}
    
    for category_folder in CLEAN_MD_DIR.iterdir():
        if not category_folder.is_dir():
            continue
        
        category = category_folder.name
        matches = []
        
        for md_file in category_folder.glob("*.md"):
            filename_lower = md_file.stem.lower()
            
            # Check if any keyword appears in filename
            for keyword in keywords:
                if keyword in filename_lower:
                    matches.append(md_file)
                    break  # Don't add same file multiple times
        
        if matches:
            relevant_files[category] = matches
    
    return relevant_files


def read_file_content(file_path: Path) -> str:
    """Read markdown file content (skip frontmatter)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2].strip()
        
        return content
    except:
        return ""


def get_filename_context(relevant_files: Dict[str, List[Path]], max_chars: int = 3000) -> str:
    """
    Read content from relevant files to provide as context
    Prioritizes beginning of each file (usually has overview/intro)
    """
    context_parts = []
    total_chars = 0
    
    for category, files in relevant_files.items():
        for file_path in files:
            if total_chars >= max_chars:
                break
            
            content = read_file_content(file_path)
            
            # Take first 1000 chars from each file (intro section)
            preview = content[:1000]
            
            context_parts.append(f"## From: {file_path.name} ({category})\n{preview}\n")
            total_chars += len(preview)
    
    if context_parts:
        return "\n---\n".join(context_parts)
    return ""


def generate_query_embedding(query: str):
    """Generate embedding for vector search"""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query"
    )
    return result['embedding']


def filter_by_filename_match(matches: list, relevant_files: Dict[str, List[Path]]) -> list:
    """
    Boost/filter results that come from files we identified by filename
    """
    # Get all relevant filenames
    relevant_filenames = set()
    for files in relevant_files.values():
        for f in files:
            relevant_filenames.add(f.name)
    
    # Separate matches into "from relevant files" and "other"
    boosted = []
    other = []
    
    for match in matches:
        file_path = match.metadata.get('file_path', '')
        filename = Path(file_path).name if file_path else ''
        
        if filename in relevant_filenames:
            # Boost score slightly for filename matches
            boosted.append(match)
        else:
            other.append(match)
    
    # Return boosted first, then others
    return boosted + other


def rerank_results(query: str, matches: list, top_n: int = 3):
    """Rerank using Cohere for precision"""
    documents = [m.metadata.get('full_text', '') for m in matches]
    
    results = co.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model='rerank-english-v3.0'
    )
    
    reranked_results = []
    for r in results.results:
        original_match = matches[r.index]
        reranked_results.append({
            "score": r.relevance_score,
            "metadata": original_match.metadata
        })
    
    return reranked_results


def hybrid_search(query: str, threshold: float = 0.70, top_k: int = 10):
    """
    Complete hybrid search pipeline:
    1. Extract keywords from query
    2. Find relevant files by filename
    3. Read content from those files as context
    4. Perform vector search
    5. Boost results from filename-matched files
    6. Rerank with Cohere
    7. Apply confidence threshold
    """
    print(f"\n{'='*60}")
    print(f"🔍 Query: {query}")
    print(f"{'='*60}\n")
    
    # Step 1: Extract keywords
    keywords = extract_keywords(query)
    print(f"📝 Keywords extracted: {', '.join(keywords)}")
    
    # Step 2: Find relevant files by filename
    relevant_files = find_relevant_files_by_name(keywords)
    
    if relevant_files:
        print(f"\n📂 Relevant files found by filename:")
        for category, files in relevant_files.items():
            print(f"  • {category}: {len(files)} files")
            for f in files[:3]:  # Show first 3
                print(f"    - {f.name}")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")
    else:
        print("\n📂 No files found by filename (will use pure vector search)")
    
    # Step 3: Get context from relevant files
    filename_context = get_filename_context(relevant_files)
    
    # Step 4: Vector search
    print(f"\n🔎 Performing vector search (top {top_k})...")
    query_embedding = generate_query_embedding(query)
    raw_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    if not raw_results.matches:
        print("❌ No results found in vector search!")
        return {
            "answer": None,
            "context": filename_context,
            "sources": []
        }
    
    # Step 5: Boost filename matches
    if relevant_files:
        print("⚡ Boosting results from filename-matched files...")
        raw_results.matches = filter_by_filename_match(raw_results.matches, relevant_files)
    
    # Step 6: Rerank
    print("🧠 Reranking with Cohere for precision...")
    final_results = rerank_results(query, raw_results.matches, top_n=5)
    
    # Step 7: Apply threshold and collect sources
    print(f"\n📊 Results (threshold: {threshold}):")
    print("="*60)
    
    sources = []
    found_valid = False
    
    for i, res in enumerate(final_results, 1):
        score = res['score']
        meta = res['metadata']
        
        if score < threshold:
            print(f"\n⚠️  Result {i}: Score {score:.4f} (below threshold - excluded)")
            continue
        
        found_valid = True
        sources.append({
            "score": score,
            "section": meta.get('section', 'Unknown'),
            "source": meta.get('source', 'Unknown'),
            "category": meta.get('category', 'Unknown'),
            "content": meta.get('full_text', '')
        })
        
        print(f"\n✅ Result {i}: Score {score:.4f}")
        print(f"   Category: {meta.get('category', 'Unknown')}")
        print(f"   Section: {meta.get('section', 'Unknown')}")
        print(f"   Source: {meta.get('source', 'Unknown')}")
        print(f"   Preview: {meta.get('text', '')[:200]}...")
    
    if not found_valid:
        print("\n❌ No high-confidence results above threshold")
    
    # Combine everything for AI
    return {
        "query": query,
        "filename_context": filename_context,
        "sources": sources,
        "keywords": keywords,
        "relevant_files": {
            cat: [str(f) for f in files] 
            for cat, files in relevant_files.items()
        }
    }


def format_for_ai(search_results: dict) -> str:
    """
    Format search results into a context block for AI consumption
    """
    parts = []
    
    parts.append(f"# User Query: {search_results['query']}\n")
    
    # Filename context
    if search_results['filename_context']:
        parts.append("## Context from Relevant Files (by filename match):")
        parts.append(search_results['filename_context'])
        parts.append("\n---\n")
    
    # Vector search results
    if search_results['sources']:
        parts.append("## Most Relevant Information (Vector Search + Reranked):\n")
        for i, source in enumerate(search_results['sources'], 1):
            parts.append(f"### Source {i} (Confidence: {source['score']:.2%})")
            parts.append(f"**From:** {source['section']} ({source['category']})")
            parts.append(f"**URL:** {source['source']}")
            parts.append(f"\n{source['content']}\n")
            parts.append("---\n")
    
    return "\n".join(parts)


if __name__ == "__main__":
    # Test queries
    test_queries = [
        "How does PNode Purchase and Transfer work",
        "How to set up a validator?",
        "What is erasure coding in Xandeum?",
        "Troubleshooting validator issues",
        "How to stake XAND tokens"
    ]
    
    print("🚀 Hybrid Search Test\n")
    
    for query in test_queries:
        results = hybrid_search(query, threshold=0.70, top_k=10)
        
        # Show formatted context for AI
        print(f"\n{'='*60}")
        print("📋 FORMATTED CONTEXT FOR AI:")
        print(f"{'='*60}")
        ai_context = format_for_ai(results)
        print(ai_context[:2000] + "..." if len(ai_context) > 2000 else ai_context)
        
        print("\n" + "="*60 + "\n")
        input("Press Enter for next query...")