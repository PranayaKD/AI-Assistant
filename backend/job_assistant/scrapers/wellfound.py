from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class WellfoundScraper(BaseScraper):
    def __init__(self):
        super().__init__("Wellfound", "https://wellfound.com")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:wellfound.com python backend developer'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'wellfound.com' in href and '/l/' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Backend Developer"
                        match = re.search(r'(https://[^&]+wellfound[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "Startup on Wellfound", title,
                                                       f"Startup position - {title}", "Varies", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Wellfound: {str(e)}")
        return jobs[:self.max_jobs]
