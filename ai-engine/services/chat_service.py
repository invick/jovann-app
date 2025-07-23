import openai
import os
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.openai_available = api_key and api_key != 'sk-dummy-key-for-testing' and not api_key.startswith('sk-your-')
        
        if self.openai_available:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            self.client = None
            logger.warning("OpenAI API key not configured - using fallback responses only")
        
        self.system_prompt = """
You are OpportunityAI, a friendly and knowledgeable military career counselor. Your goal is to help people explore military service opportunities in a non-pressured, informative way.

Key principles:
- Be conversational and human-friendly, avoid military jargon and acronyms
- Focus on lifestyle, interests, and personal goals rather than just job titles
- Explain both full-time (Active Duty) and part-time (Guard/Reserve) options
- Highlight how military skills translate to civilian careers
- Be encouraging but realistic about requirements and commitments
- Never pressure someone to join - provide information to help them decide
- Ask follow-up questions to better understand their interests and situation

When discussing careers:
- Use civilian-friendly terms instead of military acronyms (e.g., "cybersecurity specialist" not "25B")
- Explain training duration, typical day-to-day work, and promotion timeline
- Connect military experience to civilian job opportunities and salary ranges
- Mention relevant certifications and skills they would gain

If someone asks about sensitive topics like combat, deployment, or military life challenges, be honest but balanced in your response.
"""
    
    async def process_message(self, message: str, conversation_history: List[Dict] = None, user_profile: Dict = None) -> Dict[str, Any]:
        # Use fallback if OpenAI is not available
        if not self.openai_available:
            fallback_response = self._generate_fallback_response(message)
            return {
                "response": fallback_response,
                "trigger_recommendations": True,
                "confidence": 0.7,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            # Prepare conversation context
            messages = [{
                "role": "system",
                "content": self.system_prompt
            }]
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    messages.append({
                        "role": msg.get('role', 'user'),
                        "content": msg.get('content', '')
                    })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Determine if we should trigger career recommendations
            trigger_recommendations = self._should_trigger_recommendations(message, ai_response)
            
            return {
                "response": ai_response,
                "trigger_recommendations": trigger_recommendations,
                "confidence": 0.85,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            
            # Fallback response if OpenAI is unavailable
            fallback_response = self._generate_fallback_response(message)
            
            return {
                "response": fallback_response,
                "trigger_recommendations": True,
                "confidence": 0.5,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _should_trigger_recommendations(self, user_message: str, ai_response: str) -> bool:
        """Determine if we should show career recommendations based on the conversation"""
        trigger_keywords = [
            'interested in', 'like to', 'career', 'job', 'work', 'field',
            'aviation', 'cyber', 'technology', 'medical', 'engineering',
            'leadership', 'travel', 'benefits', 'training'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in trigger_keywords)
    
    def extract_interests(self, message: str) -> List[str]:
        """Extract potential interests from user message"""
        interests = []
        
        # Define interest categories and keywords
        interest_mapping = {
            'technology': ['computer', 'tech', 'cyber', 'IT', 'programming', 'software'],
            'aviation': ['flying', 'pilot', 'aircraft', 'aviation', 'air force'],
            'medical': ['medical', 'healthcare', 'doctor', 'nurse', 'health'],
            'engineering': ['engineering', 'mechanical', 'electrical', 'build'],
            'leadership': ['leadership', 'manage', 'lead', 'supervisor'],
            'travel': ['travel', 'different places', 'world', 'deploy'],
            'mechanics': ['mechanical', 'fix', 'repair', 'maintenance'],
            'communications': ['communication', 'radio', 'signals', 'network']
        }
        
        message_lower = message.lower()
        
        for interest, keywords in interest_mapping.items():
            if any(keyword in message_lower for keyword in keywords):
                interests.append(interest)
        
        return interests
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate a fallback response when OpenAI is unavailable"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm here to help you explore military career opportunities. What interests you most about potential military service?"
        
        if 'aviation' in message_lower or 'pilot' in message_lower:
            return "Aviation careers in the military are incredible! There are opportunities as pilots, air traffic controllers, aircraft mechanics, and avionics technicians. The training is world-class and leads to excellent civilian aviation careers. What specifically interests you about aviation?"
        
        if any(word in message_lower for word in ['cyber', 'technology', 'computer']):
            return "Technology and cybersecurity are huge growth areas in the military! You'd get cutting-edge training in network security, digital forensics, and IT systems. These skills are in high demand in the civilian world with great salaries. Are you interested in defensive cybersecurity or more general IT work?"
        
        if 'medical' in message_lower:
            return "Military medical careers offer amazing training opportunities! From combat medics to nurses, doctors, and medical technicians, you'd get hands-on experience that translates directly to civilian healthcare careers. What aspect of healthcare interests you most?"
        
        return "That's a great question! Military service offers many paths with excellent training and career prospects. Would you like to explore areas like technology, aviation, medical, mechanics, or leadership roles? I'm here to help you understand what might be the best fit for your interests and goals."
