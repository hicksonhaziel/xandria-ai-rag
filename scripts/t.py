# test_setup.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone
import google.generativeai as genai

load_dotenv()

# Test Pinecone
print("Testing Pinecone...")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
print(f"✅ Pinecone connected! Index stats: {index.describe_index_stats()}")

# Test Google AI Studio
print("\nTesting Google AI Studio...")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
result = genai.embed_content(
    model="models/text-embedding-004",
    content="test",
    task_type="retrieval_document"
)
print(f"✅ Google AI Studio working! Embedding dimension: {len(result['embedding'])}")

print("\n🎉 All services ready!")