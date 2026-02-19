from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__("Indeed", "https://www.indeed.com")
    
    async def scrape(self) -> List[Dict]:
        """Scrape Indeed jobs using Google search method"""
        jobs = []
        
        try:
            # Use Google to search Indeed
            search_queries = [
                'site:indeed.com "python developer" india remote',
                'site:indeed.com "django developer" remote',
                'site:indeed.com "backend developer" python remote'
            ]
            
            for query in search_queries[:1]:  # Limit queries
                google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=10"
                html = await self.fetch(google_url)
                
                if html:
                    if "consent.google.com" in html:
                        logger.warning(f"{self.name}: Blocked by Google Consent page")
                        continue

                    soup = BeautifulSoup(html, 'html.parser')
                    links_found = 0
                    
                    # Extract Indeed job links from Google results
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        # Google links often look like /url?q=https://indeed.com/...
                        if 'indeed.com' in href and ('/viewjob' in href or '/rc/clk' in href):
                            links_found += 1
                            # Extract actual Indeed URL
                            match = re.search(r'(https://[^&]+indeed[^&]+)', href)
                            if match:
                                job_url = match.group(1)
                                # Decode URL encoded characters
                                job_url = job_url.replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                                
                                title_elem = link.find('h3') or link.find('div', {'role': 'heading'})
                                title = title_elem.get_text() if title_elem else "Python Developer"
                                
                                job = self.create_job_dict(
                                    job_id=job_url.split('jk=')[-1][:20] if 'jk=' in job_url else "",
                                    company="See on Indeed",
                                    title=title,
                                    description=f"Python Backend Developer position - {title}",
                                    location="Remote/India",
                                    link=job_url
                                )
                                jobs.append(job)
                                
                                if len(jobs) >= self.max_jobs:
                                    break
                    
                    if links_found == 0:
                        logger.debug(f"{self.name}: No indeed.com links found in Google results")
                else:
                    logger.debug(f"{self.name}: Empty HTML response from Google")
                
                if len(jobs) >= self.max_jobs:
                    break
        
        except Exception as e:
            logger.error(f"Error scraping Indeed: {str(e)}")
        
        return jobs[:self.max_jobs]
