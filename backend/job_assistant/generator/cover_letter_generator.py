import os
import asyncio
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv
from config import COVERLETTER_DIR, PERSONAL_INFO, TARGET_PROFILE

load_dotenv()


class CoverLetterGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.output_dir = COVERLETTER_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self._gemini_model = None

    def _init_gemini(self):
        """Initialize Gemini model (lazy loading)"""
        if self._gemini_model is None and self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                # Using latest model name
                self._gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}")
                self._gemini_model = None

    async def generate(self, job: Dict) -> str:
        """Generate cover letter for a job - uses Gemini if available, template otherwise"""
        company = job.get('company', 'the company')
        title = job.get('title', 'Backend Developer')
        required_skills = ', '.join(job.get('required_skills', [])[:5])
        matched_skills = ', '.join(job.get('matched_skills', [])[:3])

        # Try Gemini first
        if self.api_key:
            try:
                cover_letter = await self._generate_with_gemini(company, title, required_skills, matched_skills)
                if cover_letter:
                    return await self._save_cover_letter(cover_letter, company, title)
            except Exception as e:
                print(f"Gemini generation failed, using template: {e}")

        # Fallback to template-based generation
        cover_letter = self._generate_template(company, title, required_skills, matched_skills)
        return await self._save_cover_letter(cover_letter, company, title)

    async def _generate_with_gemini(self, company: str, title: str,
                                     required_skills: str, matched_skills: str) -> str:
        """Generate cover letter using Google Gemini (FREE)"""
        self._init_gemini()

        if not self._gemini_model:
            return ""

        prompt = f"""Write a professional cover letter (150-200 words) for this job application:

Job Title: {title}
Company: {company}
Required Skills: {required_skills}
My Relevant Skills: {matched_skills}
Target Profile: {TARGET_PROFILE}

Personal Details:
- Name: {PERSONAL_INFO['name']}
- Email: {PERSONAL_INFO['email']}

The cover letter should:
- Be concise and professional
- Highlight Python/Django backend development skills
- Show enthusiasm for the role
- Mention specific relevant skills
- Be suitable for a fresher/junior role
- NOT include address or date
- Start with "Dear Hiring Manager,"
- End with "Sincerely," and name

Write ONLY the cover letter content, no additional formatting or explanations."""

        # Run Gemini in thread pool since it's synchronous
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self._gemini_model.generate_content(prompt)
        )

        return response.text.strip()

    def _generate_template(self, company: str, title: str,
                           required_skills: str, matched_skills: str) -> str:
        """Generate cover letter using template (no API needed)"""
        name = PERSONAL_INFO.get('name', 'Applicant')
        email = PERSONAL_INFO.get('email', 'email@example.com')

        skills_text = matched_skills if matched_skills else "Python, Django, REST APIs"

        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {title} position at {company}. As a passionate {TARGET_PROFILE}, I am eager to contribute my skills and enthusiasm to your team.

Through my academic journey and personal projects, I have developed strong proficiency in {skills_text}. I have hands-on experience building scalable web applications, designing RESTful APIs, and working with databases like PostgreSQL and MongoDB. My projects demonstrate my ability to write clean, maintainable code and follow best practices.

I am particularly drawn to {company} for the opportunity to work on challenging backend systems and grow as a developer. I am a quick learner, a strong collaborator, and I thrive in fast-paced environments where I can make meaningful contributions.

I would welcome the opportunity to discuss how my skills and passion for backend development align with your team's goals. Thank you for considering my application.

Sincerely,
{name}
{email}"""

        return cover_letter

    async def _save_cover_letter(self, cover_letter: str, company: str, title: str) -> str:
        """Save cover letter to file"""
        filename = f"{company.replace(' ', '_')}_{title.replace(' ', '_')[:30]}.txt"
        filename = "".join(c for c in filename if c.isalnum() or c in ['_', '-', '.'])
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cover_letter)

        return filepath
