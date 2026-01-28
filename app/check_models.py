# Save this as check_models.py and run: python check_models.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Listing available models...")
for m in client.models.list(config={"page_size": 100}):
    if "embed" in m.name:
        print(f"FOUND: {m.name}")
