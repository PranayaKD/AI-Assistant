from typing import List, Dict
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class FounditScraper(BaseScraper):
    def __init__(self):
        super().__init__("Foundit", "https://www.foundit.in")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:foundit.in python backend developer'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'foundit.in' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Backend Developer"
                        import re
                        match = re.search(r'(https://[^&]+foundit[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "See on Foundit", title,
                                                       f"Python Backend - {title}", "India", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Foundit: {str(e)}")
        return jobs[:self.max_jobs]
