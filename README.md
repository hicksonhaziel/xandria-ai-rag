# Xandria AI RAG System

> Intelligent Retrieval-Augmented Generation engine for Xandeum pNode analytics and network insights

**Part of:** [Xandria Platform](https://github.com/hicksonhaziel/xandria)  
**Live API:** [https://xandria-ai-rag.onrender.com](https://xandria-ai-rag.onrender.com)

---

## 🎯 Overview

Xandria AI is a high-performance RAG (Retrieval-Augmented Generation) system that powers intelligent conversations about the Xandeum blockchain network. Built with Python and FastAPI, it combines document retrieval, live network data, and advanced LLM capabilities to provide accurate, context-aware responses.

### Key Features

- **Smart Query Classification** - Routes queries to optimized processing paths
- **Hybrid Search** - Combines vector similarity with reranking for precision
- **Live Network Integration** - Fetches real-time pNode data when needed
- **Conversation Memory** - Maintains session-based chat history
- **Multi-Model Support** - Fallback strategy across Google Gemini models
- **Optimized Performance** - Parallel processing and smart caching

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐     │
│  │   Chat     │  │  History   │  │   Sessions   │     │
│  │  Endpoint  │  │  Endpoint  │  │   Endpoint   │     │
│  └────────────┘  └────────────┘  └──────────────┘     │
└────────────┬──────────────────────────────────────────┘
             │
    ┌────────┼────────┐
    │                 │
    ▼                 ▼
┌──────────┐    ┌──────────────┐
│  Query   │    │   Network    │
│Classifier│    │    Tools     │
└────┬─────┘    └──────┬───────┘
     │                 │
     ▼                 ▼
┌──────────────────────────────┐
│      RAG Engine              │
│  ┌──────────┐  ┌──────────┐ │
│  │  Light   │  │   Full   │ │
│  │ Search   │  │  Search  │ │
│  └──────────┘  └──────────┘ │
└────────┬─────────────────────┘
         │
    ┌────┼─────┐
    ▼    ▼     ▼
┌─────┐ ┌───┐ ┌──────┐
│Pnco │ │LLM│ │ DB   │
│ ne  │ │   │ │      │
└─────┘ └───┘ └──────┘
```

### Tech Stack

**Core:**
- Python 3.10+
- FastAPI (async web framework)
- asyncpg (PostgreSQL async driver)

**AI/ML:**
- Google Gemini (LLM)
- Pinecone (vector database)
- Cohere (reranking)
- tiktoken (token counting)

**Data Processing:**
- httpx (async HTTP client)
- asyncio (concurrent processing)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- API Keys:
  - Google AI (Gemini)
  - Pinecone
  - Cohere

### Installation

```bash
# Clone the repository
git clone https://github.com/hicksonhaziel/xandria-ai-rag.git
cd xandria-ai-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create `.env` file in the `app/` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# AI Services
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=xandria-knowledge-base
COHERE_API_KEY=your_cohere_api_key

# Xandria API
API_BASE_URL=https://xandria-eight.vercel.app/api/
```

### Database Setup

Run the SQL schema:

```bash
psql -U your_user -d your_database -f database.sql
```

### Running Locally

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`

---

## 📖 API Documentation

### Base URL
```
Production: https://xandria-ai-rag.onrender.com
Local: http://localhost:8000
```

### Endpoints

#### 1. Chat
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "unique-session-id",
  "wallet_address": "user-wallet-address",
  "message": "What is my node's performance?",
  "parent_id": null  // Optional: for threaded conversations
}
```

**Response:**
```json
{
  "success": true,
  "user_message_id": 123,
  "model_message_id": 124,
  "answer": "Your node is performing well...",
  "sources": [
    {
      "score": 0.95,
      "section": "Performance Metrics",
      "category": "Documentation",
      "content": "..."
    }
  ],
  "network_data_used": true,
  "query_type": "simple_factual",
  "processing_time": "1.23s",
  "classification": {
    "type": "simple_factual",
    "skip_rag": false,
    "skip_rerank": true,
    "use_history": true,
    "top_k": 5
  }
}
```

#### 2. Regenerate Response
```http
POST /api/chat/regenerate
Content-Type: application/json

{
  "session_id": "unique-session-id",
  "wallet_address": "user-wallet-address",
  "parent_id": 123  // ID of user message to regenerate response for
}
```

#### 3. Rate Message
```http
PATCH /api/chat/rate
Content-Type: application/json

{
  "message_id": 124,
  "rating": true  // true for positive, false for negative
}
```

#### 4. Get Conversation History
```http
GET /api/history/{session_id}
```

**Response:**
```json
{
  "success": true,
  "messages": [
    {
      "id": 123,
      "session_id": "session-123",
      "role": "user",
      "content": "What is my node performance?",
      "created_at": "2025-01-26T10:30:00Z",
      "is_active": true
    },
    {
      "id": 124,
      "role": "model",
      "content": "Your node is performing...",
      "model": "gemini-2.0-flash-exp",
      "parent_id": 123,
      "rating": true
    }
  ]
}
```

#### 5. Get User Sessions
```http
GET /api/sessions/{wallet_address}
```

**Response:**
```json
{
  "success": true,
  "sessions": [
    {
      "session_id": "session-123",
      "last_updated": "2025-01-26T10:30:00Z",
      "message_count": 10
    }
  ]
}
```

#### 6. Health Check
```http
GET /health
```

---

## 🧠 How It Works

### Query Classification

The system intelligently routes queries based on their type:

**Query Types:**

1. **Casual** (`"hi"`, `"hello"`, `"thanks"`)
   - No RAG or network fetch
   - Direct LLM response
   - Minimal context

2. **Conversational** (`"what about that?"`, `"tell me more"`)
   - Uses conversation history
   - No RAG search
   - Context-aware follow-ups

3. **Simple Factual** (`"what is XandScore?"`, `"how does staking work?"`)
   - Light search (no reranking)
   - Small top_k (5 results)
   - Fast response

4. **Complex Technical** (`"compare uptime across networks"`, `"analyze my node's performance trends"`)
   - Full search with reranking
   - Larger top_k (10 results)
   - Network data integration

### Search Pipeline

**Light Search** (for simple queries):
```
Query → Extract Keywords → Embed → Vector Search → Return Top 5
```

**Full Search** (for complex queries):
```
Query → Extract Keywords → Embed → Vector Search → 
Filename Matching → Cohere Rerank → Return Top 5
```

### Network Data Integration

The system fetches live pNode data when needed:

```python
# Detects if query needs network data
if "pnode" in query or "node performance" in query:
    # Fetch from Xandria API
    node_data = await fetch_node_info(pubkey)
    # Include in context for LLM
```

### Conversation Memory

Sessions are tracked per wallet address:
- Last 5 messages included in context
- Threaded conversations via `parent_id`
- Multiple response versions (regenerate feature)

---

## 🔧 Data Ingestion

The `scripts/` directory contains tools for building the knowledge base:

### 1. Scrape Documentation
```bash
python scripts/scrape_docs.py
```

Scrapes Xandeum documentation from official sources.

### 2. Convert to Markdown
```bash
python scripts/convert_to_markdown.py
```

Cleans and formats scraped content.

### 3. Embed and Upload
```bash
python scripts/embed_and_upload.py
```

Generates embeddings and uploads to Pinecone.

### Knowledge Base Structure
```
data/
├── raw/              # Scraped HTML/JSON
├── clean_markdown/   # Cleaned MD files
│   ├── setup/
│   ├── operations/
│   └── troubleshooting/
└── embeddings/       # Vector data
```

---

## 🎛️ Configuration

### Query Classification Thresholds

Edit `app/query_classifier.py`:

```python
CASUAL_PATTERNS = [
    r'^(hi|hello|hey|sup)\b',
    r'\b(thanks|thank you|cool)\b$',
]

CONVERSATIONAL_PATTERNS = [
    r'\b(it|this|that|those|these)\b',
    r'\b(what about|tell me more|explain)\b',
]
```

### Search Parameters

Edit `app/engine_optimized.py`:

```python
# Light search
top_k = 5
threshold = 0.70

# Full search  
top_k = 10
threshold = 0.70
rerank_top_n = 5
```

### LLM Model Fallback

Models are tried in order:

1. `gemini-2.0-flash-exp` (fastest)
2. `gemini-2.0-flash` (stable)
3. `gemini-1.5-pro` (fallback)

---

## 📊 Performance Optimization

### Parallel Processing

```python
# Fetch network data + history in parallel
network_task = asyncio.create_task(fetch_network())
history_task = asyncio.create_task(fetch_history())
network, history = await asyncio.gather(network_task, history_task)
```

### Smart Routing

- **Casual queries**: <0.5s (no RAG)
- **Simple factual**: 1-2s (light search)
- **Complex technical**: 2-4s (full search + rerank)

### Caching

- Conversation history cached per session
- Embedding cache for common queries (TODO)

---

## 🚀 Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) in the main Xandria repository for full deployment guide.

### Quick Deploy to Render

1. Connect GitHub repository
2. Set environment variables
3. Configure build:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

---

## 🧪 Testing

```bash
# Test query classification
python scripts/test_setup.py

# Test RAG pipeline
python scripts/rag_query.py "What is my node's uptime?"

# Test API endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "wallet_address": "test-wallet",
    "message": "Hello"
  }'
```

---

## 📁 Project Structure

```
xandria-ai-rag/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── database.py                # PostgreSQL async operations
│   ├── engine_optimized.py        # RAG engine
│   ├── query_classifier.py        # Query type detection
│   ├── tools_optimized.py         # Network data fetching
│   └── xandria_pnodes_apis.py    # API client
├── scripts/
│   ├── scrape_docs.py            # Documentation scraper
│   ├── convert_to_markdown.py    # Content cleaner
│   ├── embed_and_upload.py       # Vector embeddings
│   └── test_setup.py             # Testing utilities
├── data/
│   ├── raw/                      # Scraped content
│   ├── clean_markdown/           # Processed docs
│   └── embeddings/               # Vector data
├── logs/                          # Application logs
├── database.sql                   # Database schema
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add caching layer for embeddings
- [ ] Implement token usage tracking
- [ ] Add more data sources
- [ ] Improve query classification
- [ ] Add streaming responses
- [ ] Implement rate limiting

**Process:**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Main Platform**: [github.com/hicksonhaziel/xandria](https://github.com/hicksonhaziel/xandria)
- **Live Demo**: [xandria-eight.vercel.app](https://xandria-eight.vercel.app)
- **API Docs**: [xandria-ai-rag.onrender.com/docs](https://xandria-ai-rag.onrender.com/docs)

---

## 📞 Support

- **Email**: hicksonhaziel@gmail.com
- **Twitter**: [@devhickson](https://twitter.com/devhickson)
- **Discord**: [Xandeum Server](https://discord.com/invite/mGAxAuwnR9)

---

**Built with ❤️ for the Xandeum Community**
