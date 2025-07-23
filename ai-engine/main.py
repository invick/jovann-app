from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

from services.chat_service import ChatService
from services.career_matcher import CareerMatcher
from services.recommendation_engine import RecommendationEngine

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OpportunityAI Engine",
    description="AI-powered military career guidance system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chat_service = ChatService()
career_matcher = CareerMatcher()
recommendation_engine = RecommendationEngine()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    user_profile: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    recommendations: List[Dict[str, Any]] = []
    career_paths: List[Dict[str, Any]] = []
    confidence: float = 0.0

class CareerMatchRequest(BaseModel):
    interests: List[str]
    skills: List[str]
    education_level: str
    preferences: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    return {
        "message": "OpportunityAI Engine is running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "chat_service": "active",
            "career_matcher": "active",
            "recommendation_engine": "active"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Generate AI response
        response_data = await chat_service.process_message(
            message=request.message,
            conversation_history=request.conversation_history,
            user_profile=request.user_profile
        )
        
        # Get career recommendations if relevant
        recommendations = []
        career_paths = []
        
        if response_data.get('trigger_recommendations', False):
            # Extract interests and skills from conversation
            user_interests = chat_service.extract_interests(request.message)
            if user_interests:
                recommendations = await recommendation_engine.get_recommendations(
                    interests=user_interests,
                    conversation_context=request.conversation_history
                )
                
                career_paths = await career_matcher.find_matching_careers(
                    interests=user_interests,
                    skills=[],  # Extract from conversation if available
                    education_level="high_school"  # Default, can be enhanced
                )
        
        return ChatResponse(
            response=response_data['response'],
            recommendations=recommendations,
            career_paths=career_paths,
            confidence=response_data.get('confidence', 0.8)
        )
        
    except Exception as e:
        logger.error(f"Chat processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@app.post("/career-match")
async def career_match_endpoint(request: CareerMatchRequest):
    try:
        logger.info(f"Processing career match request for interests: {request.interests}")
        
        matches = await career_matcher.find_matching_careers(
            interests=request.interests,
            skills=request.skills,
            education_level=request.education_level,
            preferences=request.preferences
        )
        
        return {
            "matches": matches,
            "total_matches": len(matches),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Career matching error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to match careers")

@app.post("/recommendations")
async def recommendations_endpoint(interests: List[str], context: Optional[Dict] = None):
    try:
        logger.info(f"Generating recommendations for: {interests}")
        
        recommendations = await recommendation_engine.get_recommendations(
            interests=interests,
            conversation_context=context
        )
        
        return {
            "recommendations": recommendations,
            "total": len(recommendations),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)