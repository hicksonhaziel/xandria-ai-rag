# Xandria AI - Optimized RAG System

Smart AI assistant for Xandeum blockchain with intelligent query routing and sub-10 second response times.

## 🚀 Features

- **Smart Query Classification** - Routes queries to appropriate handlers (casual, conversational, technical)
- **Optimized RAG Pipeline** - 3-10s response times vs 30-90s previously
- **Hybrid Search** - Combines semantic search (Pinecone) with keyword matching
- **Live Network Data** - Fetches real-time pNode/vNode statistics
- **Conversation Memory** - Maintains context across chat sessions
- **PostgreSQL Storage** - Persistent chat history with versioning

## ⚡ Performance

| Query Type | Response Time | Method |
|------------|---------------|--------|
| Casual ("hi") | 0.5-1s | Direct LLM, no RAG |
| Conversational | 1-2s | History only |
| Simple factual | 3-5s | Light RAG (no reranking) |
| Complex technical | 8-10s | Full RAG with reranking |

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL database
- API Keys:
  - Google Gemini API
  - Pinecone
  - Cohere
  - Groq (optional)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd xandria-ai-ingestion
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create `.env` file in the root directory:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/xandria_db

# Vector DB
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=xandria-knowledge-base

# LLM & Embeddings
GOOGLE_API_KEY=your_google_api_key
COHERE_API_KEY=your_cohere_key
GROQ_API_KEY=your_groq_key  # Optional

# Network API
API_BASE_URL=https://xandria-eight.vercel.app/api/
```

5. **Set up database**
```bash
psql -U postgres -d xandria_db -f database.sql
```

## 🚀 Usage

**Start the server:**
```bash
cd app
python api_optimized.py

# Or with uvicorn
uvicorn api_optimized:app --host 0.0.0.0 --port 8000 --reload
```

**Test the API:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "wallet_address": "wallet123",
    "message": "what are pnodes?"
  }'
```

## 📁 Project Structure

```
xandria-ai-ingestion/
├── app/
│   ├── api_optimized.py      # FastAPI server
│   ├── engine_optimized.py   # RAG engine with query routing
│   ├── query_classifier.py   # Smart query classification
│   ├── database.py           # PostgreSQL interface
│   ├── tools.py              # Network data fetching
│   └── xandria_pnodes_apis.py
├── data/                     # Not in repo - local only
├── logs/                     # Not in repo
├── .env                      # Not in repo
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Query Classification Thresholds
Edit `query_classifier.py` to adjust classification patterns.

### RAG Settings
In `engine_optimized.py`:
- `top_k`: Number of documents to retrieve (5 for simple, 10 for complex)
- `threshold`: Minimum relevance score (default: 0.70)

## 📊 API Endpoints

### POST `/api/chat`
Main chat endpoint with smart routing.

**Request:**
```json
{
  "session_id": "uuid",
  "wallet_address": "string",
  "message": "string",
  "parent_id": null
}
```

**Response:**
```json
{
  "success": true,
  "answer": "string",
  "sources": [...],
  "query_type": "casual|conversational|simple_factual|complex_technical",
  "processing_time": "3.2s",
  "classification": {...}
}
```

### POST `/api/chat/regenerate`
Regenerate response for a message.

### GET `/api/history/{session_id}`
Get full conversation history.

### GET `/api/sessions/{wallet}`
Get all sessions for a wallet.

### Railway/Render
1. Connect GitHub repo
2. Set environment variables in dashboard
3. Deploy from `main` branch

### AWS/GCP
Use provided `requirements.txt` and configure PostgreSQL connection.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Xandeum Network for documentation and API access
- Anthropic Claude for development assistance