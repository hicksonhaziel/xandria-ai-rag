#!/usr/bin/env python3
"""
Xandria AI - Production RAG Query System (2026 Version)
Fixes: Google GenAI SDK Migration & Cohere Model ID Updates
"""

import os
import sys
from typing import Dict
from dotenv import load_dotenv

# Modern 2026 Libraries
import cohere
from google import genai
from google.genai import types

# Assuming these are your custom local files
from hybrid_search import hybrid_search, format_for_ai

load_dotenv()

# Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 1. Initialize Clients
# The new Google client automatically finds GOOGLE_API_KEY in env
google_client = genai.Client(api_key=GOOGLE_API_KEY)
co = cohere.Client(api_key=COHERE_API_KEY)

def generate_answer(query: str, context: str, use_cohere: bool = False) -> Dict:
    """
    Generates a technical answer using the provided documentation context.
    """
    system_prompt = """You are Xandria, an expert AI assistant for the Xandeum network.
RULES:
1. Use ONLY the provided context.
2. If unsure, say "I don't have enough information in the docs."
3. Cite sources (URLs/Sections) at the end.
4. Maintain exact technical command syntax."""

    user_message = f"Xandeum Documentation Context:\n{context}\n\nUser Question: {query}"

    if use_cohere:
        # FIX: Updated to 'command-r-plus-08-2024' (Stable) or 'command-a-03-2025'
        try:
            response = co.chat(
                message=user_message,
                preamble=system_prompt,
                model="command-r-plus-08-2024",
                temperature=0.3,
            )
            answer = response.text
            model_used = "Cohere Command R+ (Stable)"
        except Exception as e:
            return {"answer": f"Cohere Error: {str(e)}", "model": "Error"}
            
    else:
        # FIX: Updated to new google-genai SDK syntax
        try:
            response = google_client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                )
            )
            answer = response.text
            model_used = "Google Gemini 2.0 Flash"
        except Exception as e:
            return {"answer": f"Google Error: {str(e)}", "model": "Error"}
    
    return {"answer": answer, "model": model_used}

def ask(query: str, threshold: float = 0.70, use_cohere: bool = True):
    print("\n" + "="*60)
    print("🤖 XANDRIA AI - Xandeum Knowledge Assistant")
    print("="*60)
    
    # 1. Search & Rerank (from your hybrid_search.py)
    search_results = hybrid_search(query, threshold=threshold, top_k=10)
    
    if not search_results['sources'] and not search_results['filename_context']:
        print("\n❌ No relevant information found in Xandeum docs.")
        return
    
    # 2. Prepare Context
    context = format_for_ai(search_results)
    
    # 3. Generate Answer
    print("\n🧠 Thinking...")
    result = generate_answer(query, context, use_cohere=use_cohere)
    
    # 4. Display Result
    print("\n" + "="*60)
    print("💬 ANSWER:")
    print("="*60)
    print(result['answer'])
    
    # 5. Show Sources
    if search_results['sources']:
        print("\n" + "="*60)
        print("📚 SOURCES USED:")
        print("="*60)
        for i, source in enumerate(search_results['sources'], 1):
            if source['score'] >= threshold:
                print(f"{i}. {source['section']} (Relevance: {source['score']:.2%})")
                print(f"   URL: {source['source']}")
    
    print(f"\nEngine: {result['model']}")
    print("="*60 + "\n")

def interactive_mode():
    print("Type your Xandeum questions (or 'exit' to quit).")
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']: break
            if user_input: ask(user_input)
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ask(" ".join(sys.argv[1:]))
    else:
        interactive_mode()