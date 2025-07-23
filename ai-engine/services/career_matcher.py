from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CareerPath:
    id: str
    title: str
    branch: str
    service_type: str
    description: str
    requirements: List[str]
    training_duration: str
    civilian_translation: Dict[str, Any]
    match_keywords: List[str]
    difficulty_level: str

class CareerMatcher:
    def __init__(self):
        self.career_database = self._load_career_database()
    
    def _load_career_database(self) -> List[CareerPath]:
        """Load military career paths database"""
        return [
            CareerPath(
                id="cyber-operations",
                title="Cybersecurity Specialist",
                branch="Air Force",
                service_type="Active Duty",
                description="Protect military networks from cyber threats, conduct digital investigations, and implement security protocols.",
                requirements=["High school diploma", "Security clearance eligible", "Strong analytical skills"],
                training_duration="6-12 months",
                civilian_translation={
                    "job_titles": ["Cybersecurity Analyst", "Information Security Manager", "SOC Analyst"],
                    "average_salary": "$85,000 - $140,000",
                    "growth_outlook": "Excellent (22% growth)",
                    "certifications": ["Security+", "CISSP", "CEH"]
                },
                match_keywords=["cyber", "technology", "computer", "security", "IT", "networks"],
                difficulty_level="moderate"
            ),
            CareerPath(
                id="aviation-mechanic",
                title="Aircraft Maintenance Technician",
                branch="Navy",
                service_type="Active Duty",
                description="Maintain and repair military aircraft to ensure flight safety and mission readiness.",
                requirements=["High school diploma", "Mechanical aptitude", "Attention to detail"],
                training_duration="4-6 months",
                civilian_translation={
                    "job_titles": ["Aircraft Mechanic", "Aviation Technician", "Maintenance Supervisor"],
                    "average_salary": "$65,000 - $95,000",
                    "growth_outlook": "Good (5% growth)",
                    "certifications": ["A&P License", "FAA Certifications"]
                },
                match_keywords=["aviation", "aircraft", "mechanical", "repair", "maintenance", "hands-on"],
                difficulty_level="moderate"
            ),
            CareerPath(
                id="combat-medic",
                title="Combat Medic / Healthcare Specialist",
                branch="Army",
                service_type="Active Duty",
                description="Provide emergency medical care in field conditions and support medical operations.",
                requirements=["High school diploma", "Physical fitness", "Emotional resilience"],
                training_duration="4-6 months",
                civilian_translation={
                    "job_titles": ["Paramedic", "Emergency Medical Technician", "Medical Assistant"],
                    "average_salary": "$45,000 - $75,000",
                    "growth_outlook": "Excellent (15% growth)",
                    "certifications": ["EMT", "Paramedic License", "NREMT"]
                },
                match_keywords=["medical", "healthcare", "help people", "emergency", "first aid"],
                difficulty_level="challenging"
            ),
            CareerPath(
                id="intelligence-analyst",
                title="Intelligence Analyst",
                branch="Air Force",
                service_type="Active Duty",
                description="Analyze data and information to support military operations and national security.",
                requirements=["High school diploma", "Top Secret clearance eligible", "Analytical mindset"],
                training_duration="6-8 months",
                civilian_translation={
                    "job_titles": ["Data Analyst", "Intelligence Specialist", "Research Analyst"],
                    "average_salary": "$70,000 - $120,000",
                    "growth_outlook": "Very Good (8% growth)",
                    "certifications": ["Security+", "Certified Intelligence Professional"]
                },
                match_keywords=["analysis", "research", "investigation", "data", "intelligence", "problem-solving"],
                difficulty_level="challenging"
            ),
            CareerPath(
                id="logistics-specialist",
                title="Supply Chain / Logistics Specialist",
                branch="Army",
                service_type="Active Duty",
                description="Manage supply chains, coordinate equipment distribution, and ensure operational readiness.",
                requirements=["High school diploma", "Organizational skills", "Attention to detail"],
                training_duration="3-4 months",
                civilian_translation={
                    "job_titles": ["Supply Chain Manager", "Logistics Coordinator", "Operations Manager"],
                    "average_salary": "$55,000 - $90,000",
                    "growth_outlook": "Good (7% growth)",
                    "certifications": ["APICS", "Supply Chain Certification"]
                },
                match_keywords=["logistics", "organization", "management", "coordination", "planning"],
                difficulty_level="easy"
            )
        ]
    
    async def find_matching_careers(self, interests: List[str], skills: List[str], 
                                  education_level: str, preferences: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Find career paths that match user interests and profile"""
        try:
            matches = []
            
            for career in self.career_database:
                match_score = self._calculate_match_score(career, interests, skills)
                
                if match_score > 0.3:  # Minimum threshold for relevance
                    matches.append({
                        "career_path": {
                            "id": career.id,
                            "title": career.title,
                            "branch": career.branch,
                            "service_type": career.service_type,
                            "description": career.description,
                            "requirements": career.requirements,
                            "training_duration": career.training_duration,
                            "difficulty_level": career.difficulty_level
                        },
                        "civilian_outcome": career.civilian_translation,
                        "match_score": round(match_score, 2),
                        "match_reasons": self._get_match_reasons(career, interests, skills)
                    })
            
            # Sort by match score
            matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            return matches[:5]  # Return top 5 matches
            
        except Exception as e:
            logger.error(f"Career matching error: {str(e)}")
            return []
    
    def _calculate_match_score(self, career: CareerPath, interests: List[str], skills: List[str]) -> float:
        """Calculate how well a career path matches user interests and skills"""
        score = 0.0
        max_score = 1.0
        
        # Interest matching (70% weight)
        interest_matches = 0
        for interest in interests:
            if any(keyword.lower() in interest.lower() or interest.lower() in keyword.lower() 
                  for keyword in career.match_keywords):
                interest_matches += 1
        
        if interests:
            interest_score = min(interest_matches / len(interests), 1.0)
            score += interest_score * 0.7
        
        # Skill matching (30% weight)
        skill_matches = 0
        for skill in skills:
            if any(keyword.lower() in skill.lower() or skill.lower() in keyword.lower() 
                  for keyword in career.match_keywords):
                skill_matches += 1
        
        if skills:
            skill_score = min(skill_matches / len(skills), 1.0)
            score += skill_score * 0.3
        
        return min(score, max_score)
    
    def _get_match_reasons(self, career: CareerPath, interests: List[str], skills: List[str]) -> List[str]:
        """Get human-readable reasons why this career matches"""
        reasons = []
        
        # Check interest matches
        for interest in interests:
            matching_keywords = [kw for kw in career.match_keywords 
                               if kw.lower() in interest.lower() or interest.lower() in kw.lower()]
            if matching_keywords:
                reasons.append(f"Matches your interest in {interest}")
        
        # Check skill matches
        for skill in skills:
            matching_keywords = [kw for kw in career.match_keywords 
                               if kw.lower() in skill.lower() or skill.lower() in kw.lower()]
            if matching_keywords:
                reasons.append(f"Utilizes your {skill} skills")
        
        # Add general appeal reasons
        if career.difficulty_level == "easy":
            reasons.append("Good entry-level opportunity")
        elif career.difficulty_level == "challenging":
            reasons.append("Offers growth and development challenges")
        
        return reasons[:3]  # Limit to top 3 reasons
