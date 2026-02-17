from typing import List, Dict
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class YCScraper(BaseScraper):
    def __init__(self):
        super().__init__("Y Combinator", "https://www.ycombinator.com/jobs")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:ycombinator.com/companies python backend engineer'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'ycombinator.com' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Backend Engineer"
                        import re
                        match = re.search(r'(https://[^&]+ycombinator[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "YC Startup", title,
                                                       f"Startup role - {title}", "Varies", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Y Combinator: {str(e)}")
        return jobs[:self.max_jobs]
