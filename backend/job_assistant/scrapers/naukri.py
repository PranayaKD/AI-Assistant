from typing import List, Dict
import re
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
                if "consent.google.com" in html:
                    logger.warning(f"{self.name}: Blocked by Google Consent page")
                else:
                    soup = BeautifulSoup(html, 'html.parser')
                    links_found = 0
                    
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if 'naukri.com' in href and '/job-listings' in href:
                            links_found += 1
                            # Extract actual Naukri URL
                            match = re.search(r'(https://[^&]+naukri[^&]+)', href)
                            if match:
                                job_url = match.group(1)
                                job_url = job_url.replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                                
                                title_elem = link.find('h3') or link.find('div', {'role': 'heading'})
                                title = title_elem.get_text() if title_elem else "Python Developer"
                                
                                job = self.create_job_dict(
                                    job_id="", # Naukri IDs are complex, leave blank for hash
                                    company="See on Naukri",
                                    title=title,
                                    description=f"Backend development role - {title}",
                                    location="India",
                                    link=job_url
                                )
                                jobs.append(job)
                                
                                if len(jobs) >= self.max_jobs:
                                    break
                    
                    if links_found == 0:
                        logger.debug(f"{self.name}: No naukri.com links found in Google results")
            else:
                logger.debug(f"{self.name}: Empty HTML response from Google")
        
        except Exception as e:
            logger.error(f"Error scraping Naukri: {str(e)}")
        
        return jobs[:self.max_jobs]
