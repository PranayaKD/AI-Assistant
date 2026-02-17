import os
import asyncio
from typing import Dict
from datetime import datetime
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
from config import COVERLETTER_DIR, PERSONAL_INFO, TARGET_PROFILE

load_dotenv()


class CoverLetterGenerator:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY", "")
        self.output_dir = COVERLETTER_DIR
        
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    async def generate(self, job: Dict) -> str:
        """Generate cover letter for a job"""
        company = job.get('company', 'the company')
        title = job.get('title', 'Backend Developer')
        required_skills = ', '.join(job.get('required_skills', [])[:5])  # Top 5 skills
        matched_skills = ', '.join(job.get('matched_skills', [])[:3])  # Top 3 matched
        
        # Create prompt for cover letter
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
- NOT include address or date (will be added separately)
- Start with "Dear Hiring Manager,"
- End with "Sincerely," and name

Write ONLY the cover letter content, no additional formatting or explanations."""
        
        # Initialize chat
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"cover_letter_{datetime.now().timestamp()}",
            system_message="You are a professional cover letter writer specializing in tech job applications."
        ).with_model("openai", "gpt-4o")
        
        # Generate cover letter
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        cover_letter = response.strip()
        
        # Save to file
        filename = f"{company.replace(' ', '_')}_{title.replace(' ', '_')[:30]}.txt"
        # Remove special characters from filename
        filename = "".join(c for c in filename if c.isalnum() or c in ['_', '-', '.'])
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        return filepath
