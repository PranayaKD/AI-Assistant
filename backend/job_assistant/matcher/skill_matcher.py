import re
import logging
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class SkillMatcher:
    # Common tech skills that may appear in job descriptions beyond user's base
    COMMON_INDUSTRY_SKILLS = [
        "python", "django", "django rest framework", "rest apis",
        "postgresql", "mysql", "docker", "aws", "git",
        "authentication", "orm", "query optimization",
        "fastapi", "flask", "redis", "celery", "mongodb",
        # Additional skills the user may NOT have
        "javascript", "typescript", "react", "angular", "vue",
        "node.js", "nodejs", "java", "spring", "spring boot",
        "go", "golang", "rust", "c++", "c#", ".net",
        "kubernetes", "k8s", "terraform", "ansible", "ci/cd",
        "graphql", "grpc", "rabbitmq", "kafka", "elasticsearch",
        "html", "css", "sass", "tailwind",
        "sql", "nosql", "dynamodb", "cassandra",
        "azure", "gcp", "google cloud", "heroku",
        "linux", "nginx", "apache",
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "pandas", "numpy", "data science",
        "agile", "scrum", "jira",
        "microservices", "serverless", "lambda",
        "jenkins", "github actions", "gitlab ci",
        "selenium", "pytest", "unit testing",
    ]

    def __init__(self, skills_base: List[str]):
        self.skills_base = [skill.lower() for skill in skills_base]
        self.skills_base_set = set(self.skills_base)

        # Build a combined list: user skills + common industry skills (deduplicated)
        all_detectable = set(self.skills_base)
        for s in self.COMMON_INDUSTRY_SKILLS:
            all_detectable.add(s.lower())
        self.all_detectable = list(all_detectable)
        self.all_patterns = self._create_patterns(self.all_detectable)

    def _create_patterns(self, skills: List[str]) -> Dict[str, re.Pattern]:
        """Create regex patterns for each skill"""
        patterns = {}
        for skill in skills:
            pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
            patterns[skill] = pattern
        return patterns

    def extract_all_skills_from_text(self, text: str) -> Set[str]:
        """Extract ALL recognizable skills from job description (not just user's)."""
        if not text:
            return set()

        found_skills = set()
        for skill in self.all_detectable:
            pattern = self.all_patterns.get(skill)
            if pattern and pattern.search(text):
                found_skills.add(skill)
        return found_skills

    def match_job(self, job: Dict) -> Dict:
        """Match job against skill base and calculate percentage"""
        description = job.get('description', '')
        title = job.get('title', '')

        # Combine title and description for better matching
        full_text = f"{title} {description}"

        # Extract ALL skills from job description (including ones user doesn't have)
        required_skills = self.extract_all_skills_from_text(full_text)

        if not required_skills:
            # If no skills found, check if it's a Python/Backend role by title
            if any(keyword in title.lower() for keyword in ['python', 'django', 'backend']):
                required_skills = {'python'}  # Default minimum

        # Match: intersection of required skills with USER's skill base
        matched_skills = required_skills.intersection(self.skills_base_set)
        # Missing: skills the job wants that the user does NOT have
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

        # Log details for transparency
        logger.debug(f"Matching Job: {title}")
        logger.debug(f"  Required: {job['required_skills']}")
        logger.debug(f"  Matched:  {job['matched_skills']}")
        logger.debug(f"  Match %:  {job['match_percentage']}%")

        return job
