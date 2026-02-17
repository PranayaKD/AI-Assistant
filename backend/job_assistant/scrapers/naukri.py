from typing import List, Dict
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class NaukriScraper(BaseScraper):
    def __init__(self):
        super().__init__("Naukri", "https://www.naukri.com")
    
    async def scrape(self) -> List[Dict]:
        """Scrape Naukri jobs using Google search"""
        jobs = []
        
        try:
            search_query = 'site:naukri.com "python developer" OR "django developer" fresher'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=20"
            
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'naukri.com/job-listings' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Python Developer"
                        
                        # Extract job URL
                        import re
                        match = re.search(r'(https://[^&]+naukri[^&]+)', href)
                        if match:
                            job_url = match.group(1)
                            
                            job = self.create_job_dict(
                                job_id="",
                                company="See on Naukri",
                                title=title,
                                description=f"Backend development role - {title}",
                                location="India",
                                link=job_url
                            )
                            jobs.append(job)
                            
                            if len(jobs) >= self.max_jobs:
                                break
        
        except Exception as e:
            logger.error(f"Error scraping Naukri: {str(e)}")
        
        return jobs[:self.max_jobs]
