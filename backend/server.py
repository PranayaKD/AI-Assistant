from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys
import json
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection (optional - graceful fallback)
mongo_client = None
db = None

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'ai_assistant_db')
    mongo_client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=3000)
    db = mongo_client[db_name]
    logger.info(f"MongoDB configured: {mongo_url}")
except Exception as e:
    logger.warning(f"MongoDB not available: {e}. Running without database.")

# Job Assistant paths
JOB_ASSISTANT_DIR = ROOT_DIR / 'job_assistant'
HISTORY_FILE = JOB_ASSISTANT_DIR / 'database' / 'jobs_history.json'
COVERLETTER_DIR = JOB_ASSISTANT_DIR / 'output' / 'coverletters'

# Lifespan context manager (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app):
    # Startup
    yield
    # Shutdown
    if mongo_client:
        mongo_client.close()

# Create the main app
app = FastAPI(
    title="AI Job Search Assistant API",
    description="Backend API for the AI-powered Job Search Assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware — must be added BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ─── Models ───────────────────────────────────────────────────────────
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class JobResponse(BaseModel):
    job_id: str = ""
    company: str = ""
    title: str = ""
    description: str = ""
    location: str = ""
    link: str = ""
    portal: str = ""
    required_skills: List[str] = []
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    match_percentage: float = 0.0
    cover_letter_generated: str = "No"
    cover_letter_path: str = ""
    date_found: str = ""

class DashboardStats(BaseModel):
    total_jobs_found: int = 0
    matched_jobs: int = 0
    highest_match: float = 0.0
    portals_scraped: int = 0
    cover_letters_generated: int = 0
    last_run: str = "Never"

class SearchRequest(BaseModel):
    task: str = "morning"  # "morning" or "reminder"


# ─── Helper Functions ──────────────────────────────────────────────────
def load_job_history() -> dict:
    """Load job history from JSON file"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading job history: {e}")
    return {"jobs": []}


def get_cover_letters() -> List[str]:
    """Get list of generated cover letters"""
    try:
        if COVERLETTER_DIR.exists():
            return [f.name for f in COVERLETTER_DIR.iterdir() if f.suffix == '.txt']
    except Exception as e:
        logger.error(f"Error listing cover letters: {e}")
    return []


def read_cover_letter(filename: str) -> str:
    """Read content of a cover letter file"""
    try:
        filepath = COVERLETTER_DIR / filename
        if filepath.exists():
            return filepath.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error reading cover letter: {e}")
    return ""


# ─── API Routes ────────────────────────────────────────────────────────
@api_router.get("/")
async def root():
    return {
        "message": "AI Job Search Assistant API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "mongodb": "connected" if db is not None else "not connected"
    }


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    mongo_status = "disconnected"
    if db is not None:
        try:
            await mongo_client.admin.command('ping')
            mongo_status = "connected"
        except:
            mongo_status = "disconnected"

    return {
        "status": "healthy",
        "mongodb": mongo_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@api_router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    history = load_job_history()
    jobs = history.get('jobs', [])
    cover_letters = get_cover_letters()

    # Calculate stats
    total = len(jobs)
    matched = len([j for j in jobs if j.get('match_percentage', 0) >= 50])
    highest = max([j.get('match_percentage', 0) for j in jobs], default=0)
    portals = len(set(j.get('portal', '') for j in jobs))
    last_run = jobs[-1].get('date_found', 'Never') if jobs else "Never"

    return DashboardStats(
        total_jobs_found=total,
        matched_jobs=matched,
        highest_match=highest,
        portals_scraped=portals,
        cover_letters_generated=len(cover_letters),
        last_run=last_run
    )


@api_router.get("/jobs", response_model=List[JobResponse])
async def get_jobs():
    """Get all scraped and matched jobs"""
    history = load_job_history()
    jobs = history.get('jobs', [])

    return [
        JobResponse(
            job_id=job.get('hash', job.get('job_id', '')),
            company=job.get('company', 'Unknown'),
            title=job.get('title', 'Unknown'),
            description=job.get('description', ''),
            location=job.get('location', ''),
            link=job.get('link', ''),
            portal=job.get('portal', 'Unknown'),
            required_skills=job.get('required_skills', []),
            matched_skills=job.get('matched_skills', []),
            missing_skills=job.get('missing_skills', []),
            match_percentage=job.get('match_percentage', 0),
            cover_letter_generated=job.get('cover_letter_generated', 'No'),
            cover_letter_path=job.get('cover_letter_path', ''),
            date_found=job.get('date_found', '')
        )
        for job in jobs
    ]


@api_router.get("/cover-letters")
async def list_cover_letters():
    """List all generated cover letters"""
    letters = get_cover_letters()
    return {"cover_letters": letters, "count": len(letters)}


@api_router.get("/cover-letters/{filename}")
async def get_cover_letter(filename: str):
    """Get content of a specific cover letter"""
    content = read_cover_letter(filename)
    if not content:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return {"filename": filename, "content": content}


@api_router.post("/search")
async def trigger_search(request: SearchRequest):
    """Trigger a job search (runs the job assistant)"""
    import subprocess

    main_py = JOB_ASSISTANT_DIR / 'main.py'
    if not main_py.exists():
        raise HTTPException(status_code=500, detail="Job assistant main.py not found")

    try:
        # Run the job search in a subprocess
        result = subprocess.Popen(
            [sys.executable, str(main_py), request.task],
            cwd=str(JOB_ASSISTANT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return {
            "message": f"Job search ({request.task}) triggered!",
            "status": "running",
            "pid": result.pid,
            "note": "This runs in the background. Check /api/jobs for results."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start search: {str(e)}")


# Status endpoints (MongoDB - optional)
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)

    if db is not None:
        try:
            doc = status_obj.model_dump()
            doc['timestamp'] = doc['timestamp'].isoformat()
            await db.status_checks.insert_one(doc)
        except Exception as e:
            logger.warning(f"MongoDB write failed: {e}")

    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    if db is None:
        return []

    try:
        status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
        for check in status_checks:
            if isinstance(check.get('timestamp'), str):
                check['timestamp'] = datetime.fromisoformat(check['timestamp'])
        return status_checks
    except Exception as e:
        logger.warning(f"MongoDB read failed: {e}")
        return []


# Include the router in the main app
app.include_router(api_router)