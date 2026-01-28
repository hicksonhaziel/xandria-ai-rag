import os
import re
from pathlib import Path
from typing import List, Dict, Optional, AsyncGenerator
from dotenv import load_dotenv
import cohere
from pinecone import Pinecone
from google import genai
from google.genai import types
import tiktoken
import asyncio
from query_classifier import classifier

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "xandria-knowledge-base")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CLEAN_MD_DIR = Path("data/clean_markdown")

google_client = genai.Client(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
co = cohere.Client(api_key=COHERE_API_KEY)
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
            model="gemini-embedding-001",
            contents=query,
            config=types.EmbedContentConfig(output_dimensionality=768)
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

async def light_search(query: str, top_k: int = 5) -> Dict:
    """
    Lightweight search - NO reranking, smaller top_k
    For simple factual queries
    """
    keywords = extract_keywords(query)
    
    # Parallel ops
    relevant_files_task = asyncio.create_task(
        asyncio.to_thread(find_relevant_files, keywords)
    )
    embedding_task = asyncio.create_task(generate_query_embedding_async(query))
    
    relevant_files, query_embedding = await asyncio.gather(
        relevant_files_task,
        embedding_task
    )
    
    filename_context = get_filename_context(relevant_files)
    raw_results = await query_pinecone_async(query_embedding, top_k)
    
    if not raw_results.matches:
        return {
            "sources": [],
            "filename_context": filename_context,
            "keywords": keywords
        }
    
    # NO reranking - just use top results directly
    sources = []
    for match in raw_results.matches[:top_k]:
        if match.score >= 0.70:  # Use Pinecone score directly
            meta = match.metadata
            sources.append({
                "score": match.score,
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

async def full_search(query: str, threshold: float = 0.70, top_k: int = 10) -> Dict:
    """
    Full search with reranking - for complex queries
    """
    keywords = extract_keywords(query)
    
    relevant_files_task = asyncio.create_task(
        asyncio.to_thread(find_relevant_files, keywords)
    )
    embedding_task = asyncio.create_task(generate_query_embedding_async(query))
    
    relevant_files, query_embedding = await asyncio.gather(
        relevant_files_task,
        embedding_task
    )
    
    filename_context = get_filename_context(relevant_files)
    raw_results = await query_pinecone_async(query_embedding, top_k)
    
    if not raw_results.matches:
        return {
            "sources": [],
            "filename_context": filename_context,
            "keywords": keywords
        }
    
    if relevant_files:
        raw_results.matches = filter_by_filename_match(raw_results.matches, relevant_files)
    
    # Full reranking
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
        for msg in conversation_history[-5:]:  # Reduced from 10 to 5
            role = msg['role'].upper()
            content = msg['content'][:300]  # Reduced from 500
            parts.append(f"**{role}:** {content}\n")
    
    return "\n".join(parts)

def format_casual_context(conversation_history: List[Dict]) -> str:
    """Minimal context for casual queries"""
    if not conversation_history:
        return ""
    
    parts = ["# Recent Conversation:\n"]
    for msg in conversation_history[-3:]:  # Only last 3 messages
        role = msg['role'].upper()
        content = msg['content'][:150]
        parts.append(f"**{role}:** {content}\n")
    
    return "\n".join(parts)

async def generate_answer_streaming(
    query: str,
    context: str,
    query_type: str
):
    """Generate answer optimized by query type with fallback models"""
    
    # Different system instructions based on query type
    if query_type == "casual":
        system_instruction = """You are Xandria, a friendly AI assistant for Xandeum blockchain.
Keep responses natural and conversational. Be brief for simple greetings."""
    
    elif query_type == "conversational":
        system_instruction = """You are Xandria, the AI assistant for Xandeum blockchain.
Focus on the conversation history to answer the user's follow-up question.
Reference previous context naturally."""
    
    else:  # simple_factual or complex_technical
        system_instruction = """You are Xandria, the AI assistant for Xandeum blockchain network.

RULES:
1. If context is provided, use ONLY that information
2. If no context but network data is available, explain based on live data
3. If neither, provide general blockchain knowledge
5. Preserve exact technical syntax for commands
6. Be concise and technical"""
    
    user_message = f"Context:\n{context}\n\nUser Question: {query}" if context else query
    
    # Try models in order: flash-exp (fastest) -> flash (stable) -> pro (fallback)
    models = [
        "gemini-3-flash-preview",
        "gemini-2.5-flash", 
        "gemini-3-flash"
    ]
    
    for model in models:
        try:
            response = google_client.models.generate_content(
                model=model,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3 if query_type in ["simple_factual", "complex_technical"] else 0.7,
                )
            )

            if response.text:
                return response.text
        
        except Exception as e:
            # If this is the last model, raise error
            if model == models[-1]:
                raise Exception(f"All models failed. Last error: {str(e)}")
            # Otherwise try next model
            continue
    
    return "I'm sorry, I couldn't generate a response."

class RAGEngine:
    async def query(
        self,
        user_query: str,
        conversation_history: List[Dict] = None,
        network_context: str = "",
        threshold: float = 0.70
    ) -> Dict:
        """
        OPTIMIZED RAG pipeline with smart routing
        Returns: {answer: str, sources: List[Dict], model: str, query_type: str, processing_time: float}
        """
        import time
        start_time = time.time()
        
        # STEP 1: Classify query (< 0.1s)
        classification = classifier.classify(user_query)
        query_type = classification['type']
        
        sources = []
        context = ""
        
        # STEP 2: Route based on classification
        if classification['skip_rag']:
            # CASUAL or CONVERSATIONAL - no RAG needed
            if classification['use_history'] and conversation_history:
                context = format_casual_context(conversation_history)
            # No search needed - direct to LLM
            
        else:
            # SIMPLE_FACTUAL or COMPLEX_TECHNICAL - needs RAG
            if classification['skip_rerank']:
                # Light search for simple queries
                search_results = await light_search(user_query, top_k=classification['top_k'])
            else:
                # Full search for complex queries
                search_results = await full_search(user_query, threshold=threshold, top_k=classification['top_k'])
            
            sources = search_results.get('sources', [])
            context = format_context(
                search_results,
                conversation_history or [] if classification['use_history'] else [],
                network_context
            )
        
        # STEP 3: Generate answer
        answer = await generate_answer_streaming(user_query, context, query_type)
        
        processing_time = time.time() - start_time
        
        return {
            "answer": answer,
            "sources": sources,
            "model": "gemini-3-flash-preview",
            "query_type": query_type,
            "processing_time": processing_time,
            "classification": classification
        }

rag_engine = RAGEngine()
