import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
import cohere
from pinecone import Pinecone
from google import genai
from google.genai import types
import tiktoken
import asyncio
import httpx

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "xandria-knowledge-base")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CLEAN_MD_DIR = Path("data/clean_markdown")

google_client = genai.Client(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
co = cohere.Client(api_key=COHERE_API_KEY)  # Standard client, we'll wrap it
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def extract_keywords(query: str) -> List[str]:
    stop_words = {
        'how', 'what', 'when', 'where', 'why', 'does', 'is', 'are', 'the', 
        'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'do', 'i', 'my', 'me', 'work', 'can', 'get', 'make', 'use'
    }
    words = re.findall(r'\b\w+\b', query.lower())
    return [w for w in words if w not in stop_words and len(w) > 2]

def find_relevant_files(keywords: List[str]) -> Dict[str, List[Path]]:
    relevant_files = {}
    for category_folder in CLEAN_MD_DIR.iterdir():
        if not category_folder.is_dir():
            continue
        matches = []
        for md_file in category_folder.glob("*.md"):
            filename_lower = md_file.stem.lower()
            if any(keyword in filename_lower for keyword in keywords):
                matches.append(md_file)
                break
        if matches:
            relevant_files[category_folder.name] = matches
    return relevant_files

def read_file_content(file_path: Path) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content
    except:
        return ""

def get_filename_context(relevant_files: Dict[str, List[Path]], max_chars: int = 3000) -> str:
    context_parts = []
    total_chars = 0
    for category, files in relevant_files.items():
        for file_path in files:
            if total_chars >= max_chars:
                break
            content = read_file_content(file_path)
            preview = content[:1000]
            context_parts.append(f"## {file_path.name} ({category})\n{preview}\n")
            total_chars += len(preview)
    return "\n---\n".join(context_parts) if context_parts else ""

async def generate_query_embedding_async(query: str):
    """Async wrapper for embedding generation"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: google_client.models.embed_content(
            model="models/text-embedding-004",
            contents=query
        )
    )
    return result.embeddings[0].values

async def query_pinecone_async(vector, top_k: int):
    """Async wrapper for Pinecone query"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
    )

def filter_by_filename_match(matches: list, relevant_files: Dict[str, List[Path]]) -> list:
    relevant_filenames = set()
    for files in relevant_files.values():
        for f in files:
            relevant_filenames.add(f.name)
    boosted = []
    other = []
    for match in matches:
        file_path = match.metadata.get('file_path', '')
        filename = Path(file_path).name if file_path else ''
        if filename in relevant_filenames:
            boosted.append(match)
        else:
            other.append(match)
    return boosted + other

async def rerank_results_async(query: str, matches: list, top_n: int = 5):
    """Async reranking with Cohere API"""
    documents = [m.metadata.get('full_text', '') for m in matches]
    
    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: co.rerank(
            query=query,
            documents=documents,
            top_n=top_n,
            model='rerank-english-v3.0'
        )
    )
    
    reranked = []
    for r in response.results:
        original = matches[r.index]
        reranked.append({
            "score": r.relevance_score,
            "metadata": original.metadata
        })
    return reranked

async def hybrid_search(query: str, threshold: float = 0.70, top_k: int = 10) -> Dict:
    """Optimized hybrid search with parallel operations"""
    keywords = extract_keywords(query)
    
    # Run file search and embedding generation in parallel
    relevant_files_task = asyncio.create_task(
        asyncio.to_thread(find_relevant_files, keywords)
    )
    embedding_task = asyncio.create_task(generate_query_embedding_async(query))
    
    relevant_files, query_embedding = await asyncio.gather(
        relevant_files_task,
        embedding_task
    )
    
    # Get filename context (fast operation)
    filename_context = get_filename_context(relevant_files)
    
    # Query Pinecone
    raw_results = await query_pinecone_async(query_embedding, top_k)
    
    if not raw_results.matches:
        return {
            "sources": [],
            "filename_context": filename_context,
            "keywords": keywords
        }
    
    # Filter by filename match
    if relevant_files:
        raw_results.matches = filter_by_filename_match(raw_results.matches, relevant_files)
    
    # Rerank asynchronously
    final_results = await rerank_results_async(query, raw_results.matches, top_n=5)
    
    sources = []
    for res in final_results:
        if res['score'] >= threshold:
            meta = res['metadata']
            sources.append({
                "score": res['score'],
                "section": meta.get('section', 'Unknown'),
                "source": meta.get('source', 'Unknown'),
                "category": meta.get('category', 'Unknown'),
                "content": meta.get('full_text', '')
            })
    
    return {
        "sources": sources,
        "filename_context": filename_context,
        "keywords": keywords
    }

def format_context(
    search_results: Dict,
    conversation_history: List[Dict],
    network_context: str = ""
) -> str:
    parts = []
    
    if network_context:
        parts.append("# Live Network Data:\n")
        parts.append(network_context)
        parts.append("\n---\n")
    
    if search_results.get('filename_context'):
        parts.append("# Documentation Context:\n")
        parts.append(search_results['filename_context'])
        parts.append("\n---\n")
    
    if search_results.get('sources'):
        parts.append("# Relevant Information:\n")
        for i, source in enumerate(search_results['sources'], 1):
            parts.append(f"## Source {i} (Confidence: {source['score']:.2%})")
            parts.append(f"**Section:** {source['section']}")
            parts.append(f"**Category:** {source['category']}")
            parts.append(f"\n{source['content']}\n")
            parts.append("---\n")
    
    if conversation_history:
        parts.append("# Conversation History:\n")
        for msg in conversation_history[-10:]:
            role = msg['role'].upper()
            content = msg['content'][:500]
            parts.append(f"**{role}:** {content}\n")
    
    return "\n".join(parts)

async def generate_answer_streaming(
    query: str,
    context: str,
    has_rag_context: bool
):
    """Generate answer with streaming support"""
    system_instruction = """You are Xandria, the AI assistant for Xandeum blockchain network.

RULES:
1. If context is provided, use ONLY that information
2. If no context but network data is available, explain based on live data
3. If neither, provide general blockchain knowledge with previous context(if provided) or your general blockchain knowledge 
4. Cite sources when available
5. Preserve exact technical syntax for commands
6. Be concise and technical"""

    disclaimer = "" if has_rag_context else "\n\nNote: This answer is based on general blockchain knowledge as specific Xandeum documentation was not found for this query."
    
    user_message = f"Context:\n{context}\n\nUser Question: {query}"
    
    try:
        # Use streaming for faster perceived response
        response = google_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
            )
        )

        answer_text = response.text if response.text else "I'm sorry, I couldn't generate a response."
        return answer_text + disclaimer
        
    except Exception as e:
        raise Exception(f"Generation failed: {str(e)}")

class RAGEngine:
    async def query(
        self,
        user_query: str,
        conversation_history: List[Dict] = None,
        network_context: str = "",
        threshold: float = 0.70
    ) -> Dict:
        """
        Optimized RAG pipeline with parallel operations
        Returns: {answer: str, sources: List[Dict], model: str}
        """
        # Run search and answer generation in parallel
        search_task = asyncio.create_task(
            hybrid_search(user_query, threshold=threshold)
        )
        
        # Wait for search to complete first
        search_results = await search_task
        
        # Format context
        context = format_context(
            search_results,
            conversation_history or [],
            network_context
        )
        
        has_context = bool(search_results.get('sources') or network_context)
        
        # Generate answer
        answer = await generate_answer_streaming(user_query, context, has_context)
        
        return {
            "answer": answer,
            "sources": search_results.get('sources', []),
            "model": "gemini-3-flash-preview"
        }

rag_engine = RAGEngine()