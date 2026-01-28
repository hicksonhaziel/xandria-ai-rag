import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

res = client.models.embed_content(
    model="gemini-embedding-001", 
    contents="test", 
    config={'output_dimensionality': 768}
)
print(f"Confirmed Dimension: {len(res.embeddings[0].values)}")
