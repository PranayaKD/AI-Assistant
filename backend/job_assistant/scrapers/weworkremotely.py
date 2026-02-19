from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class WeWorkRemotelyScraper(BaseScraper):
    def __init__(self):
        super().__init__("We Work Remotely", "https://weworkremotely.com")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:weworkremotely.com python backend developer'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'weworkremotely.com' in href and '/jobs/' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Backend Developer"
                        match = re.search(r'(https://[^&]+weworkremotely[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "See on We Work Remotely", title,
                                                       f"Remote position - {title}", "Remote", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping We Work Remotely: {str(e)}")
        return jobs[:self.max_jobs]
