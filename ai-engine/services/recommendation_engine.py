from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.recommendation_templates = self._load_recommendation_templates()
    
    def _load_recommendation_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load recommendation templates for different interests"""
        return {
            "technology": {
                "next_questions": [
                    "Are you more interested in cybersecurity or general IT support?",
                    "Do you prefer working with networks, programming, or hardware?",
                    "Have you worked with any specific technologies or programming languages?"
                ],
                "action_items": [
                    "Explore cybersecurity specialist roles",
                    "Look into Signal/IT specialist positions",
                    "Consider Air Force or Space Force for tech opportunities"
                ],
                "learning_resources": [
                    "Learn about CompTIA Security+ certification",
                    "Research military cybersecurity training programs",
                    "Check out basic networking and programming courses"
                ]
            },
            "aviation": {
                "next_questions": [
                    "Are you interested in being a pilot or working on aircraft maintenance?",
                    "Do you prefer fixed-wing aircraft or helicopters?",
                    "Are you comfortable with heights and mechanical work?"
                ],
                "action_items": [
                    "Research pilot training requirements",
                    "Explore aircraft maintenance careers",
                    "Look into Air Traffic Control opportunities"
                ],
                "learning_resources": [
                    "Learn about different types of military aircraft",
                    "Research civilian aviation career paths",
                    "Study basic aerodynamics and aircraft systems"
                ]
            },
            "medical": {
                "next_questions": [
                    "Are you interested in direct patient care or medical support roles?",
                    "Do you prefer emergency medicine or specialized care?",
                    "Are you planning to pursue medical school in the future?"
                ],
                "action_items": [
                    "Explore combat medic training",
                    "Research medical laboratory specialist roles",
                    "Look into dental or veterinary technician positions"
                ],
                "learning_resources": [
                    "Get EMT or First Aid certification",
                    "Research military medical training programs",
                    "Study basic anatomy and medical terminology"
                ]
            },
            "leadership": {
                "next_questions": [
                    "Do you prefer leading small teams or large organizations?",
                    "Are you interested in operational leadership or administrative roles?",
                    "Do you have any previous leadership experience?"
                ],
                "action_items": [
                    "Consider Officer Candidate School",
                    "Explore Non-Commissioned Officer paths",
                    "Research leadership development programs"
                ],
                "learning_resources": [
                    "Study military leadership principles",
                    "Learn about different officer career paths",
                    "Practice communication and team management skills"
                ]
            },
            "mechanics": {
                "next_questions": [
                    "Do you prefer working on vehicles, aircraft, or ships?",
                    "Are you interested in electronics or purely mechanical systems?",
                    "Do you enjoy troubleshooting and problem-solving?"
                ],
                "action_items": [
                    "Explore automotive maintenance roles",
                    "Research aircraft or ship maintenance careers",
                    "Look into electronics repair specialties"
                ],
                "learning_resources": [
                    "Learn basic automotive or mechanical skills",
                    "Study electronics and electrical systems",
                    "Research ASE or other industry certifications"
                ]
            }
        }
    
    async def get_recommendations(self, interests: List[str], 
                                conversation_context: Optional[List] = None) -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on user interests"""
        try:
            recommendations = []
            
            for interest in interests:
                if interest in self.recommendation_templates:
                    template = self.recommendation_templates[interest]
                    
                    recommendation = {
                        "category": interest.title(),
                        "type": "career_guidance",
                        "priority": "high",
                        "content": {
                            "next_questions": template["next_questions"][:2],  # Limit to 2 questions
                            "suggested_actions": template["action_items"][:3],  # Limit to 3 actions
                            "learning_resources": template["learning_resources"][:2]  # Limit to 2 resources
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    recommendations.append(recommendation)
            
            # Add general recommendations if no specific interests matched
            if not recommendations:
                recommendations.append(self._get_general_recommendation())
            
            # Add exploration recommendation
            recommendations.append(self._get_exploration_recommendation())
            
            return recommendations[:3]  # Limit to 3 recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            return [self._get_fallback_recommendation()]
    
    def _get_general_recommendation(self) -> Dict[str, Any]:
        """Get a general recommendation for users without specific interests"""
        return {
            "category": "General Exploration",
            "type": "career_guidance",
            "priority": "medium",
            "content": {
                "next_questions": [
                    "What activities do you enjoy in your free time?",
                    "Do you prefer working with people, technology, or hands-on tasks?"
                ],
                "suggested_actions": [
                    "Take a military career aptitude assessment",
                    "Speak with recruiters from different branches",
                    "Research the differences between Active Duty, Guard, and Reserves"
                ],
                "learning_resources": [
                    "Explore military.com career exploration tools",
                    "Watch day-in-the-life videos of different military jobs"
                ]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_exploration_recommendation(self) -> Dict[str, Any]:
        """Get a recommendation to explore more options"""
        return {
            "category": "Next Steps",
            "type": "action_items",
            "priority": "medium",
            "content": {
                "next_questions": [
                    "Would you like to see a 4-year career forecast for any of these paths?",
                    "Are you interested in part-time service (Guard/Reserves) or full-time?"
                ],
                "suggested_actions": [
                    "Save interesting career paths for later review",
                    "Connect with current service members in your areas of interest",
                    "Research education benefits and how they work"
                ],
                "learning_resources": [
                    "Learn about military education benefits (GI Bill, tuition assistance)",
                    "Research how military experience translates to civilian careers"
                ]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_fallback_recommendation(self) -> Dict[str, Any]:
        """Get a fallback recommendation when other methods fail"""
        return {
            "category": "Getting Started",
            "type": "career_guidance",
            "priority": "high",
            "content": {
                "next_questions": [
                    "What are your main interests or hobbies?",
                    "What kind of work environment do you prefer?"
                ],
                "suggested_actions": [
                    "Explore different military career categories",
                    "Consider your long-term career goals",
                    "Think about what type of training appeals to you"
                ],
                "learning_resources": [
                    "Research basic information about military service",
                    "Learn about different service branches and their specialties"
                ]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
