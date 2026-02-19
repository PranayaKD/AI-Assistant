from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class InstahyreScraper(BaseScraper):
    def __init__(self):
        super().__init__("Instahyre", "https://www.instahyre.com")
    
    async def scrape(self) -> List[Dict]:
        """Scrape Instahyre jobs"""
        jobs = []
        
        try:
            search_query = 'site:instahyre.com "python" backend developer'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'instahyre.com' in href and '/job/' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Backend Developer"
                        
                        match = re.search(r'(https://[^&]+instahyre[^&]+)', href)
                        if match:
                            job_url = match.group(1)
                            
                            job = self.create_job_dict(
                                job_id="",
                                company="See on Instahyre",
                                title=title,
                                description=f"Python Backend position - {title}",
                                location="India/Remote",
                                link=job_url
                            )
                            jobs.append(job)
                            
                            if len(jobs) >= self.max_jobs:
                                break
        
        except Exception as e:
            logger.error(f"Error scraping Instahyre: {str(e)}")
        
        return jobs[:self.max_jobs]
