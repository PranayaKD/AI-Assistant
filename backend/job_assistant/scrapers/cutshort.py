from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class CutshortScraper(BaseScraper):
    def __init__(self):
        super().__init__("Cutshort", "https://cutshort.io")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:cutshort.io python developer remote'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'cutshort.io' in href and '/jobs/' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Python Developer"
                        match = re.search(r'(https://[^&]+cutshort[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "See on Cutshort", title, 
                                                       f"Backend role - {title}", "India", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Cutshort: {str(e)}")
        return jobs[:self.max_jobs]
