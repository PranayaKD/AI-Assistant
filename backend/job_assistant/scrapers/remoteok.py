from typing import List, Dict
import logging
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class RemoteOKScraper(BaseScraper):
    def __init__(self):
        super().__init__("Remote OK", "https://remoteok.com")
    
    async def scrape(self) -> List[Dict]:
        """Scrape Remote OK using their API"""
        jobs = []
        
        try:
            # Remote OK public API
            api_url = "https://remoteok.com/api"
            data = await self.fetch_json(api_url)
            
            if isinstance(data, list):
                for item in data[1:]:  # Skip first item (metadata)
                    if not isinstance(item, dict):
                        continue
                    
                    tags = item.get('tags', [])
                    position = item.get('position', '')
                    
                    # Filter for Python/Backend roles
                    if any(tag.lower() in ['python', 'django', 'backend'] for tag in tags) or \
                       any(keyword in position.lower() for keyword in ['python', 'django', 'backend']):
                        
                        job = self.create_job_dict(
                            job_id=str(item.get('id', '')),
                            company=item.get('company', 'Unknown'),
                            title=position,
                            description=item.get('description', position),
                            location='Remote',
                            link=item.get('url', f"https://remoteok.com/remote-jobs/{item.get('id', '')}")
                        )
                        jobs.append(job)
                        
                        if len(jobs) >= self.max_jobs:
                            break
        
        except Exception as e:
            logger.error(f"Error scraping Remote OK: {str(e)}")
        
        return jobs[:self.max_jobs]
