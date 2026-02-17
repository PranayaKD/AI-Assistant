from typing import List, Dict
import logging
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class RemotiveScraper(BaseScraper):
    def __init__(self):
        super().__init__("Remotive", "https://remotive.com")
    
    async def scrape(self) -> List[Dict]:
        """Scrape Remotive using their API"""
        jobs = []
        
        try:
            # Remotive public API
            api_url = "https://remotive.com/api/remote-jobs?category=software-dev"
            data = await self.fetch_json(api_url)
            
            if isinstance(data, dict) and 'jobs' in data:
                for item in data['jobs']:
                    title = item.get('title', '')
                    
                    # Filter for Python/Backend roles
                    if any(keyword in title.lower() for keyword in ['python', 'django', 'backend', 'engineer']):
                        job = self.create_job_dict(
                            job_id=str(item.get('id', '')),
                            company=item.get('company_name', 'Unknown'),
                            title=title,
                            description=item.get('description', title),
                            location='Remote',
                            link=item.get('url', '')
                        )
                        jobs.append(job)
                        
                        if len(jobs) >= self.max_jobs:
                            break
        
        except Exception as e:
            logger.error(f"Error scraping Remotive: {str(e)}")
        
        return jobs[:self.max_jobs]
