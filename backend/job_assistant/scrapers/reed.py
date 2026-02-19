from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class ReedScraper(BaseScraper):
    def __init__(self):
        super().__init__("Reed.co.uk", "https://www.reed.co.uk")
    
    async def scrape(self) -> List[Dict]:
        jobs = []
        try:
            search_query = 'site:reed.co.uk python developer backend'
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}&num=15"
            html = await self.fetch(google_url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'reed.co.uk' in href and '/jobs/' in href:
                        title_elem = link.find('h3')
                        title = title_elem.get_text() if title_elem else "Python Developer"
                        match = re.search(r'(https://[^&]+)', href)
                        if match:
                            job = self.create_job_dict("", "See on Reed", title,
                                                       f"UK position - {title}", "UK", match.group(1))
                            jobs.append(job)
                            if len(jobs) >= self.max_jobs:
                                break
        except Exception as e:
            logger.error(f"Error scraping Reed: {str(e)}")
        return jobs[:self.max_jobs]
