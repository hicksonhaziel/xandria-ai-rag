import os
from typing import List, Dict, Optional
from datetime import datetime
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
    
    async def save_message(
        self,
        session_id: str,
        wallet_address: str,
        role: str,
        content: str,
        model: Optional[str] = None,
        parent_id: Optional[int] = None,
        message_version: int = 1
    ) -> int:
        query = """
            INSERT INTO chat_messages 
            (session_id, wallet_address, role, content, model, parent_id, message_version)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query, session_id, wallet_address, role, content, 
                model, parent_id, message_version
            )
            return row['id']
    
    async def deactivate_old_responses(self, parent_id: int):
        query = """
            UPDATE chat_messages 
            SET is_active = false 
            WHERE parent_id = $1 AND role = 'model'
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, parent_id)
    
    async def get_next_version(self, parent_id: int) -> int:
        query = """
            SELECT COALESCE(MAX(message_version), 0) + 1 as next_version
            FROM chat_messages 
            WHERE parent_id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, parent_id)
            return row['next_version']
    
    async def get_message(self, message_id: int) -> Optional[Dict]:
        query = "SELECT * FROM chat_messages WHERE id = $1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, message_id)
            return dict(row) if row else None
    
    async def get_conversation_history(
        self, 
        session_id: str, 
        limit: int = 10
    ) -> List[Dict]:
        query = """
            SELECT * FROM chat_messages 
            WHERE session_id = $1 AND is_active = true
            ORDER BY created_at DESC
            LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, session_id, limit)
            return [dict(row) for row in reversed(rows)]
    
    async def get_full_thread(self, session_id: str) -> List[Dict]:
        query = """
            SELECT * FROM chat_messages 
            WHERE session_id = $1 AND is_active = true
            ORDER BY created_at ASC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, session_id)
            return [dict(row) for row in rows]
    
    async def get_sessions(self, wallet_address: str) -> List[Dict]:
        query = """ 
            WITH session_stats AS (
                SELECT 
                    session_id,
                    MAX(created_at) as last_updated,
                    COUNT(*) FILTER (WHERE role = 'user') as message_count,
                    MIN(created_at) FILTER (WHERE role = 'user') as first_message_time
                FROM chat_messages
                WHERE wallet_address = $1
                GROUP BY session_id
            ),
            first_messages AS (
                SELECT DISTINCT ON (cm.session_id)
                    cm.session_id,
                    cm.content as first_message
                FROM chat_messages cm
                INNER JOIN session_stats ss ON cm.session_id = ss.session_id
                WHERE cm.wallet_address = $1 
                    AND cm.role = 'user'
                    AND cm.created_at = ss.first_message_time
                ORDER BY cm.session_id, cm.created_at ASC
            )
            SELECT 
                ss.session_id,
                ss.last_updated,
                ss.message_count,
                COALESCE(
                    CASE 
                        WHEN LENGTH(fm.first_message) <= 60 THEN fm.first_message
                        ELSE SUBSTRING(fm.first_message FROM 1 FOR 60) || '...'
                    END,
                    'New conversation'
                ) as summary
            FROM session_stats ss
            LEFT JOIN first_messages fm ON ss.session_id = fm.session_id
            ORDER BY ss.last_updated DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, wallet_address)
            return [dict(row) for row in rows]
    
    async def update_rating(self, message_id: int, rating: bool):
        query = "UPDATE chat_messages SET rating = $1 WHERE id = $2"
        async with self.pool.acquire() as conn:
            await conn.execute(query, rating, message_id)

db = Database()