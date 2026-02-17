from abc import ABC, abstractmethod
from typing import List, Dict
import aiohttp
import asyncio
import logging
from config import HEADERS, REQUEST_TIMEOUT, JOBS_PER_PORTAL

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(self, name: str, portal_url: str):
        self.name = name
        self.portal_url = portal_url
        self.headers = HEADERS.copy()
        self.timeout = REQUEST_TIMEOUT
        self.max_jobs = JOBS_PER_PORTAL
    
    @abstractmethod
    async def scrape(self) -> List[Dict]:
        """Scrape jobs from the portal"""
        pass
    
    async def fetch(self, url: str, method: str = 'GET', **kwargs) -> str:
        """Fetch content from URL"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                if method == 'GET':
                    async with session.get(url, headers=self.headers, **kwargs) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                            return ""
                elif method == 'POST':
                    async with session.post(url, headers=self.headers, **kwargs) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                            return ""
        except asyncio.TimeoutError:
            logger.warning(f"{self.name}: Timeout fetching {url}")
            return ""
        except Exception as e:
            logger.error(f"{self.name}: Error fetching {url}: {str(e)}")
            return ""
    
    async def fetch_json(self, url: str, method: str = 'GET', **kwargs) -> Dict:
        """Fetch JSON content from URL"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                if method == 'GET':
                    async with session.get(url, headers=self.headers, **kwargs) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                            return {}
                elif method == 'POST':
                    async with session.post(url, headers=self.headers, **kwargs) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                            return {}
        except asyncio.TimeoutError:
            logger.warning(f"{self.name}: Timeout fetching {url}")
            return {}
        except Exception as e:
            logger.error(f"{self.name}: Error fetching {url}: {str(e)}")
            return {}
    
    def create_job_dict(self, job_id: str, company: str, title: str, 
                       description: str, location: str, link: str) -> Dict:
        """Create standardized job dictionary"""
        return {
            "job_id": job_id,
            "company": company,
            "title": title,
            "description": description,
            "location": location,
            "link": link,
            "portal": self.name,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0
        }
