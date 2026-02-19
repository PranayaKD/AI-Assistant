from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class UndutchablesScraper(BaseScraper):
    def __init__(self):
        super().__init__("Undutchables", "https://undutchables.nl")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:undutchables.nl software developer python'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'undutchables.nl' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Software Developer"
                        match = re.search(r'(https://[^&]+undutchables[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "See on Undutchables", title,
                                                       f"Netherlands position - {title}", "Netherlands", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Undutchables: {str(e)}")
        return jobs[:self.max_jobs]
