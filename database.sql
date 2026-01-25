
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    wallet_address VARCHAR(64) NOT NULL,
    role VARCHAR(20) NOT NULL,           -- 'user' or 'model'
    content TEXT NOT NULL,
    model VARCHAR(50) DEFAULT NULL,      -- Added for your future use
    parent_id INTEGER REFERENCES chat_messages(id), 
    message_version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    rating BOOLEAN DEFAULT NULL,         
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX idx_chat_session_time ON chat_messages (session_id, created_at);
CREATE INDEX idx_chat_parent_id ON chat_messages (parent_id);
CREATE INDEX idx_chat_rating ON chat_messages (rating) WHERE rating IS NOT NULL;
CREATE INDEX idx_wallet_address ON chat_messages (wallet_address);