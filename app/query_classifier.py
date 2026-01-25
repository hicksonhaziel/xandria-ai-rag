import re
from typing import Dict, Literal

QueryType = Literal["casual", "conversational", "simple_factual", "complex_technical"]

class QueryClassifier:
    """
    Fast query classification to route requests appropriately
    NO ML needed - simple keyword matching is fast and effective
    """
    
    def __init__(self):
        # Casual greetings and acknowledgments
        self.casual_patterns = [
            r'^(hi|hello|hey|sup|yo)\b',
            r'^(thanks|thank you|ty|thx)\b',
            r'^(ok|okay|sure|yes|no|yep|nope)\b',
            r'^(bye|goodbye|see you|later)\b',
            r'^(how are you|what\'s up|wassup)\b',
        ]
        
        # Conversational - references to chat history
        self.conversational_patterns = [
            r'\b(earlier|before|previous|last|above|you said|you mentioned)\b',
            r'\b(continue|more about|tell me more|what about)\b',
            r'\b(that|this|those|these)\s+(answer|response|message|explanation)\b',
            r'^(what did|can you|could you)\s+(i|we)\s+(say|ask|talk)',
            r'\b(again|remind me|recall|remember)\b',
            r'\bmy (name|question|issue)\b',
            r'\bwhat was\b',
            r'\byou just\b',
        ]
        
        # Complex technical - multiple keywords, commands, configurations
        self.complex_indicators = [
            r'\b(how (do|can) i|step by step|configure|setup|install|deploy)\b',
            r'\b(troubleshoot|debug|error|issue|problem|not working)\b',
            r'\b(command|script|code|example|tutorial)\b',
            r'\b(and|also|additionally|furthermore)\b.*\b(and|also)\b',  # Multiple questions
            r'\b(compare|difference|versus|vs|better)\b',
            r'\b(architecture|implementation|best practice|production)\b',
        ]
        
        # Simple factual - single concept questions
        self.simple_indicators = [
            r'^what is (a|an|the)\b',
            r'^(define|explain|describe)\b',
            r'^(who|what|where|when)\b',
            r'\?$',  # Single question mark
        ]
        
    def classify(self, query: str) -> Dict[str, any]:
        """
        Classify query and return routing decision
        Returns: {
            "type": QueryType,
            "confidence": float,
            "skip_rag": bool,
            "use_history": bool,
            "top_k": int,
            "skip_rerank": bool
        }
        """
        query_lower = query.lower().strip()
        
        # 1. Check casual (highest priority - fastest route)
        if len(query_lower) < 20 and any(re.search(p, query_lower) for p in self.casual_patterns):
            return {
                "type": "casual",
                "confidence": 0.95,
                "skip_rag": True,
                "use_history": False,
                "top_k": 0,
                "skip_rerank": True,
                "reason": "Greeting/acknowledgment detected"
            }
        
        # 2. Check conversational (uses history, no RAG)
        if any(re.search(p, query_lower) for p in self.conversational_patterns):
            return {
                "type": "conversational",
                "confidence": 0.85,
                "skip_rag": True,
                "use_history": True,
                "top_k": 0,
                "skip_rerank": True,
                "reason": "References to conversation history"
            }
        
        # 3. Check complex technical (full RAG)
        complexity_score = sum(1 for p in self.complex_indicators if re.search(p, query_lower))
        if complexity_score >= 2 or len(query_lower) > 100:
            return {
                "type": "complex_technical",
                "confidence": 0.80,
                "skip_rag": False,
                "use_history": True,
                "top_k": 10,
                "skip_rerank": False,
                "reason": f"Complex query (score: {complexity_score}, length: {len(query_lower)})"
            }
        
        # 4. Default to simple factual (light RAG)
        simple_match = any(re.search(p, query_lower) for p in self.simple_indicators)
        if simple_match or len(query_lower) < 50:
            return {
                "type": "simple_factual",
                "confidence": 0.75,
                "skip_rag": False,
                "use_history": False,
                "top_k": 5,
                "skip_rerank": True,  # Skip reranking for simple queries
                "reason": "Simple factual question"
            }
        
        # 5. Fallback to complex if unsure
        return {
            "type": "complex_technical",
            "confidence": 0.60,
            "skip_rag": False,
            "use_history": True,
            "top_k": 8,
            "skip_rerank": False,
            "reason": "Uncertain - defaulting to full search"
        }

classifier = QueryClassifier()