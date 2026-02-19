import json
import hashlib
from datetime import datetime, date
from typing import List, Dict, Set
import os
from config import HISTORY_FILE


class JobDatabase:
    def __init__(self):
        self.history_file = HISTORY_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create history file if it doesn't exist"""
        if not os.path.exists(self.history_file):
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump({"jobs": []}, f)
    
    def _generate_job_hash(self, job: Dict) -> str:
        """Generate unique hash for job link"""
        link = job.get('link', '')
        return hashlib.md5(link.encode()).hexdigest()
    
    def load_history(self) -> Dict:
        """Load job history from file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {"jobs": []}
    
    def save_history(self, history: Dict):
        """Save job history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2, default=str)
    
    def filter_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Filter out duplicate jobs based on history"""
        history = self.load_history()
        existing_hashes = {job.get('hash') for job in history.get('jobs', [])}
        
        unique_jobs = []
        for job in jobs:
            job_hash = self._generate_job_hash(job)
            if job_hash not in existing_hashes:
                job['hash'] = job_hash
                unique_jobs.append(job)
        
        return unique_jobs
    
    def save_jobs(self, jobs: List[Dict]):
        """Save new jobs to history"""
        history = self.load_history()
        
        for job in jobs:
            job_record = {
                'hash': job.get('hash'),
                'link': job.get('link'),
                'company': job.get('company'),
                'title': job.get('title'),
                'portal': job.get('portal'),
                'date_found': datetime.now().isoformat(),
                'match_percentage': job.get('match_percentage')
            }
            history['jobs'].append(job_record)
        
        self.save_history(history)
    
    def get_today_jobs_count(self) -> int:
        """Get count of jobs found today"""
        history = self.load_history()
        today = date.today().isoformat()
        
        count = 0
        for job in history.get('jobs', []):
            job_date = job.get('date_found', '')[:10]  # Get date part only
            if job_date == today:
                count += 1
        
        return count
