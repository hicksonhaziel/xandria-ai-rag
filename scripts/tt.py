import os
import cohere  # pip install cohere
from dotenv import load_dotenv
from pinecone import Pinecone
import google.generativeai as genai

load_dotenv()

# Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY") # Get a free key at dashboard.cohere.com
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "xandria-knowledge-base")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize
genai.configure(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
co = cohere.Client(COHERE_API_KEY)

def generate_query_embedding(query: str):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query"
    )
    return result['embedding']

def rerank_results(query: str, matches: list):
    """
    Takes the raw Pinecone matches and re-scores them 
    based on actual relevance to the query.
    """
    # Extract the text from the Pinecone metadata
    documents = [m.metadata.get('full_text', '') for m in matches]
    
    # Call Cohere Rerank
    # Model 'rerank-english-v3.0' is state-of-the-art
    results = co.rerank(
        query=query,
        documents=documents,
        top_n=3,
        model='rerank-english-v3.0'
    )
    
    reranked_results = []
    for r in results.results:
        original_match = matches[r.index]
        reranked_results.append({
            "score": r.relevance_score, # This is your new, highly accurate score
            "metadata": original_match.metadata
        })
    
    return reranked_results

def search(query: str, threshold: float = 0.75):
    print(f"\n🔍 Query: {query}")
    print("="*60)
    
    # 1. Get more results than you need (Top 10) to give the reranker room to work
    query_embedding = generate_query_embedding(query)
    raw_results = index.query(vector=query_embedding, top_k=10, include_metadata=True)
    
    if not raw_results.matches:
        print("❌ No initial results found!")
        return

    # 2. Rerank the results
    print("🧠 Reranking for high-precision...")
    final_results = rerank_results(query, raw_results.matches)
    
    # 3. Apply the "No Mistakes" Threshold
    found_valid = False
    for i, res in enumerate(final_results, 1):
        score = res['score']
        
        if score < threshold:
            print(f"\n⚠️ Result {i} blocked (Score {score:.4f} below threshold {threshold})")
            continue
            
        found_valid = True
        meta = res['metadata']
        print(f"\n✅ Result {i} (NEW Rerank Score: {score:.4f})")
        print(f"Section: {meta.get('section', 'Unknown')}")
        print(f"Content: {meta.get('full_text', '')[:1000]}...")
        print("-" * 30)

    if not found_valid:
        print("\n❌ No high-confidence information found for this query.")

if __name__ == "__main__":
    search("How does PNode Purchase and Transfer work", threshold=0.70)