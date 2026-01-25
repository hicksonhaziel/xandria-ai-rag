from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from database import db
from engine_optimized import rag_engine
from tools import network_tools
import asyncio

app = FastAPI(title="Xandria AI API - Optimized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

class ChatRequest(BaseModel):
    session_id: str
    wallet_address: str
    message: str
    parent_id: Optional[int] = None

class RegenerateRequest(BaseModel):
    session_id: str
    wallet_address: str
    parent_id: int

class RateRequest(BaseModel):
    message_id: int
    rating: bool

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    OPTIMIZED chat endpoint with parallel processing
    Flow:
    1. Save user message
    2. Classify query
    3. Fetch network data + history in parallel (if needed)
    4. Run optimized RAG
    5. Save model response
    """
    try:
        # Save user message (fast)
        user_msg_id = await db.save_message(
            session_id=request.session_id,
            wallet_address=request.wallet_address,
            role="user",
            content=request.message,
            parent_id=request.parent_id
        )
        
        # Run network fetch and history fetch in parallel
        network_task = asyncio.create_task(
            network_tools.fetch_relevant_data(request.message)
        )
        history_task = asyncio.create_task(
            db.get_conversation_history(request.session_id, limit=5)  # Reduced from 10
        )
        
        # Wait for both
        tool_result, history = await asyncio.gather(network_task, history_task)
        
        network_context = tool_result['context'] if tool_result['fetched'] else ""
        
        # Run RAG (now optimized with query classification)
        result = await rag_engine.query(
            user_query=request.message,
            conversation_history=history,
            network_context=network_context,
            threshold=0.70
        )
        
        # Save model response
        model_msg_id = await db.save_message(
            session_id=request.session_id,
            wallet_address=request.wallet_address,
            role="model",
            content=result['answer'],
            model=result['model'],
            parent_id=user_msg_id,
            message_version=1
        )
        
        return {
            "success": True,
            "user_message_id": user_msg_id,
            "model_message_id": model_msg_id,
            "answer": result['answer'],
            "sources": result['sources'],
            "network_data_used": tool_result['fetched'],
            "query_type": result['query_type'],
            "processing_time": f"{result['processing_time']:.2f}s",
            "classification": result['classification']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/regenerate")
async def regenerate(request: RegenerateRequest):
    """
    Regenerate response - also optimized
    """
    try:
        parent_msg = await db.get_message(request.parent_id)
        if not parent_msg:
            raise HTTPException(status_code=404, detail="Parent message not found")
        
        if parent_msg['wallet_address'] != request.wallet_address:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        # Deactivate old responses
        await db.deactivate_old_responses(request.parent_id)
        next_version = await db.get_next_version(request.parent_id)
        
        # Parallel fetch
        network_task = asyncio.create_task(
            network_tools.fetch_relevant_data(parent_msg['content'])
        )
        history_task = asyncio.create_task(
            db.get_conversation_history(request.session_id, limit=5)
        )
        
        tool_result, history = await asyncio.gather(network_task, history_task)
        network_context = tool_result['context'] if tool_result['fetched'] else ""
        
        # Run optimized RAG
        result = await rag_engine.query(
            user_query=parent_msg['content'],
            conversation_history=history,
            network_context=network_context,
            threshold=0.70
        )
        
        model_msg_id = await db.save_message(
            session_id=request.session_id,
            wallet_address=request.wallet_address,
            role="model",
            content=result['answer'],
            model=result['model'],
            parent_id=request.parent_id,
            message_version=next_version
        )
        
        return {
            "success": True,
            "message_id": model_msg_id,
            "answer": result['answer'],
            "version": next_version,
            "sources": result['sources'],
            "query_type": result['query_type'],
            "processing_time": f"{result['processing_time']:.2f}s"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/chat/rate")
async def rate_message(request: RateRequest):
    """Update rating for a specific message"""
    try:
        await db.update_rating(request.message_id, request.rating)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    """Get full conversation thread for a session"""
    try:
        messages = await db.get_full_thread(session_id)
        return {
            "success": True,
            "messages": messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{wallet}")
async def get_sessions(wallet: str):
    """Get all chat sessions for a wallet"""
    try:
        sessions = await db.get_sessions(wallet)
        return {
            "success": True,
            "sessions": sessions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "optimized"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)