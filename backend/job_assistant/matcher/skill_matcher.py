import re
from typing import Dict, List, Set


class SkillMatcher:
    def __init__(self, skills_base: List[str]):
        self.skills_base = [skill.lower() for skill in skills_base]
        self.skills_patterns = self._create_patterns()
    
    def _create_patterns(self) -> Dict[str, re.Pattern]:
        """Create regex patterns for each skill"""
        patterns = {}
        for skill in self.skills_base:
            # Create word boundary pattern for accurate matching
            pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
            patterns[skill] = pattern
        return patterns
    
    def extract_skills_from_text(self, text: str) -> Set[str]:
        """Extract skills from job description"""
        if not text:
            return set()
        
        found_skills = set()
        text_lower = text.lower()
        
        for skill in self.skills_base:
            pattern = self.skills_patterns.get(skill)
            if pattern and pattern.search(text):
                found_skills.add(skill)
        
        return found_skills
    
    def match_job(self, job: Dict) -> Dict:
        """Match job against skill base and calculate percentage"""
        description = job.get('description', '')
        title = job.get('title', '')
        
        # Combine title and description for better matching
        full_text = f"{title} {description}"
        
        # Extract required skills from job description
        required_skills = self.extract_skills_from_text(full_text)
        
        if not required_skills:
            # If no skills found, check if it's a Python/Backend role by title
            if any(keyword in title.lower() for keyword in ['python', 'django', 'backend']):
                required_skills = {'python'}  # Default minimum
        
        # Match with our skills
        matched_skills = required_skills.intersection(set(self.skills_base))
        missing_skills = required_skills - matched_skills
        
        # Calculate match percentage
        if required_skills:
            match_percentage = (len(matched_skills) / len(required_skills)) * 100
        else:
            match_percentage = 0
        
        # Update job with matching info
        job['required_skills'] = sorted(list(required_skills))
        job['matched_skills'] = sorted(list(matched_skills))
        job['missing_skills'] = sorted(list(missing_skills))
        job['match_percentage'] = round(match_percentage, 2)
        
        return job
