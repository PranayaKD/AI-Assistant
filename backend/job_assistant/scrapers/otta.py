from typing import List, Dict
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class OttaScraper(BaseScraper):
    def __init__(self):
        super().__init__("Otta", "https://otta.com")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:otta.com python backend engineer'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'otta.com' in href and '/jobs/' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Backend Engineer"
                        import re
                        match = re.search(r'(https://[^&]+otta[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "See on Otta", title,
                                                       f"Startup role - {title}", "Varies", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Otta: {str(e)}")
        return jobs[:self.max_jobs]
