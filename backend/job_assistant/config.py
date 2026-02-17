import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Personal Information (Update these with your details)
PERSONAL_INFO = {
    "name": "Your Name",
    "email": "your.email@example.com",
    "phone": "+91-XXXXXXXXXX",
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "portfolio": "https://yourportfolio.com"
}

# Target Profile
TARGET_PROFILE = "Fresher Python Backend / Django Developer"

# Skills Base
SKILLS_BASE = [
    "Python",
    "Django",
    "Django REST Framework",
    "REST APIs",
    "PostgreSQL",
    "MySQL",
    "Docker",
    "AWS",
    "Git",
    "Authentication",
    "ORM",
    "Query Optimization",
    "FastAPI",
    "Flask",
    "Redis",
    "Celery",
    "MongoDB"
]

# Locations
TARGET_LOCATIONS = [
    "India",
    "Remote",
    "UK",
    "Netherlands",
    "Global Remote",
    "Anywhere"
]

# Job Titles to Match
JOB_TITLES = [
    "Python Developer",
    "Django Developer",
    "Backend Developer",
    "Associate Software Engineer",
    "Graduate Software Engineer",
    "Trainee SWE",
    "Junior Python Developer",
    "Junior Backend Engineer",
    "Software Engineer",
    "Backend Engineer"
]

# API Keys and Tokens
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
EXCEL_DIR = os.path.join(OUTPUT_DIR, "excel")
COVERLETTER_DIR = os.path.join(OUTPUT_DIR, "coverletters")
HISTORY_FILE = os.path.join(DATABASE_DIR, "jobs_history.json")

# Create directories if they don't exist
for directory in [DATABASE_DIR, OUTPUT_DIR, EXCEL_DIR, COVERLETTER_DIR]:
    os.makedirs(directory, exist_ok=True)

# Job Search Settings
MAX_JOBS_PER_RUN = 35
MIN_MATCH_PERCENTAGE = 50
JOBS_PER_PORTAL = 5  # Limit per portal to avoid overwhelming

# Scraper Settings
REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# Excel Column Headers
EXCEL_COLUMNS = [
    "S.No",
    "Date",
    "Job ID / Ref No.",
    "Company Name",
    "Job Role / Title",
    "Job Link / Portal Link",
    "Job Portal (Site)",
    "Status",
    "Interview Mode",
    "Interview Date",
    "Mail Sent (Yes/No)",
    "Cold Email Sent (Yes/No)",
    "Follow Up Mail (Yes/No)",
    "Response Received (Yes/No)",
    "Remarks / Notes",
    "Exact Skills Required",
    "Match %",
    "Resume Changes Needed",
    "Cover Letter Generated"
]

# Scheduler Settings (IST)
MORNING_RUN_TIME = "03:30"  # 9:00 AM IST in UTC
REMINDER_TIME = "08:45"  # 2:15 PM IST in UTC

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
