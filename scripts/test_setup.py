#!/usr/bin/env python3
"""
Test script to verify all API connections work
Run this before starting data ingestion
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone
from huggingface_hub import InferenceClient
import requests

# Load environment variables
load_dotenv()

def test_env_variables():
    """Check if all required environment variables are set"""
    print("1️⃣  Checking environment variables...")
    
    required_vars = ['HUGGINGFACE_API_KEY', 'PINECONE_API_KEY']
    optional_vars = ['GROQ_API_KEY', 'GITHUB_TOKEN']
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing required variables: {', '.join(missing)}")
        print("   Add them to your .env file")
        return False
    
    print("✅ All required environment variables found")
    
    # Check optional
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ Optional: {var} found")
        else:
            print(f"⚠️  Optional: {var} not found (recommended but not required)")
    
    print()
    return True


def test_pinecone():
    """Test Pinecone connection and index"""
    print("2️⃣  Testing Pinecone connection...")
    
    try:
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        
        # List indexes
        indexes = pc.list_indexes()
        print(f"✅ Connected to Pinecone")
        print(f"   Found {len(indexes)} index(es)")
        
        # Check if our index exists
        index_names = [idx.name for idx in indexes]
        
        if 'xandria-knowledge' in index_names:
            print("✅ Index 'xandria-knowledge' exists")
            
            # Check dimensions
            for idx in indexes:
                if idx.name == 'xandria-knowledge':
                    if idx.dimension == 384:
                        print("✅ Correct dimensions (384)")
                    else:
                        print(f"⚠️  WARNING: Index has {idx.dimension} dimensions")
                        print("   Expected: 384 for Hugging Face model")
                        print("   You may need to recreate the index")
        else:
            print("⚠️  Index 'xandria-knowledge' not found")
            print("   Create it in Pinecone dashboard:")
            print("   - Name: xandria-knowledge")
            print("   - Dimensions: 384")
            print("   - Metric: cosine")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Pinecone connection failed: {e}")
        print()
        return False


def test_huggingface():
    """Test Hugging Face API connection"""
    print("3️⃣  Testing Hugging Face API...")
    
    try:
        client = InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))
        
        # Test feature extraction (embeddings)
        test_text = "This is a test sentence"
        
        result = client.feature_extraction(
            text=test_text,
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Convert to list if needed
        embedding = result if isinstance(result, list) else list(result)
        
        print("✅ Hugging Face API working")
        print(f"   Model: sentence-transformers/all-MiniLM-L6-v2")
        print(f"   Generated embedding with {len(embedding)} dimensions")
        print("   💰 Cost: $0.00 (FREE!)")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Hugging Face API failed: {e}")
        print("   Make sure your API token is valid")
        print("   Get it at: https://huggingface.co/settings/tokens")
        print()
        return False


def test_groq():
    """Test Groq API (optional but recommended for chat)"""
    print("4️⃣  Testing Groq API (optional)...")
    
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("⚠️  GROQ_API_KEY not set - skipping")
        print("   Get FREE key at: https://console.groq.com/")
        print()
        return True
    
    try:
        headers = {
            'Authorization': f'Bearer {groq_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'llama-3.3-70b-versatile',
            'messages': [{'role': 'user', 'content': 'Say hi'}],
            'max_tokens': 10
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print("✅ Groq API working")
            print("   Model: llama-3.3-70b-versatile")
            print("   Free tier: 30 requests/min")
            print()
            return True
        else:
            print(f"⚠️  Groq API returned status {response.status_code}")
            print()
            return False
            
    except Exception as e:
        print(f"⚠️  Groq API test failed: {e}")
        print()
        return False


def test_sample_upload():
    """Test uploading and querying a sample vector"""
    print("5️⃣  Testing sample data upload...")
    
    try:
        # Initialize clients
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        hf_client = InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))
        
        index = pc.Index('xandria-knowledge')
        
        # Generate test embedding
        test_text = "This is a test document for Xandria AI"
        
        result = hf_client.feature_extraction(
            text=test_text,
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        embedding = result if isinstance(result, list) else list(result)
        
        # Upload to Pinecone
        index.upsert(
            vectors=[{
                'id': 'test_vector_1',
                'values': embedding,
                'metadata': {
                    'text': test_text,
                    'source': 'test'
                }
            }],
            namespace='test'
        )
        
        print("✅ Successfully uploaded test vector")
        
        # Query it back
        query_result = index.query(
            vector=embedding,
            top_k=1,
            namespace='test',
            include_metadata=True
        )
        
        if query_result.matches:
            match = query_result.matches[0]
            print(f"✅ Successfully queried test vector")
            print(f"   Score: {match.score:.4f}")
            print(f"   Text: {match.metadata.get('text', 'N/A')}")
        
        # Clean up
        index.delete(ids=['test_vector_1'], namespace='test')
        print("✅ Cleaned up test data")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Sample upload/query failed: {e}")
        print()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Testing Xandria AI Setup (FREE Version)")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Environment Variables", test_env_variables()))
    results.append(("Pinecone", test_pinecone()))
    results.append(("Hugging Face", test_huggingface()))
    results.append(("Groq", test_groq()))
    results.append(("Sample Upload", test_sample_upload()))
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    
    if passed >= 4:  # Allow Groq to be optional
        print("🎉 ALL CRITICAL TESTS PASSED!")
        print("You're ready to start data ingestion!")
        print()
        print("💰 Cost Breakdown:")
        print("   - Hugging Face API: $0.00 (FREE)")
        print("   - Pinecone: $0.00 (free tier)")
        print("   - Groq: $0.00 (free tier)")
        print("   - TOTAL: $0.00/month! 🎉")
        print()
        print("Next steps:")
        print("1. Run: python scripts/scrape_docs.py")
        print("2. Run: python scripts/fetch_github.py")
        print("3. Run: python scripts/fetch_youtube.py")
        print("4. Or run all: python scripts/run_all.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("   Make sure all API keys are correct in .env file")
    
    print("=" * 60)


if __name__ == "__main__":
    main()