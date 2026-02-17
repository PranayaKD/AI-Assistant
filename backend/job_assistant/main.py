#!/usr/bin/env python3
import sys
import asyncio
import logging
from datetime import datetime
from typing import List, Dict
import traceback

from config import (
    MAX_JOBS_PER_RUN,
    MIN_MATCH_PERCENTAGE,
    SKILLS_BASE,
    LOG_LEVEL
)
from matcher.skill_matcher import SkillMatcher
from generator.excel_writer import ExcelWriter
from generator.cover_letter_generator import CoverLetterGenerator
from notifier.telegram_bot import TelegramNotifier
from database.db_manager import JobDatabase

# Import all scrapers
from scrapers.indeed import IndeedScraper
from scrapers.naukri import NaukriScraper
from scrapers.instahyre import InstahyreScraper
from scrapers.cutshort import CutshortScraper
from scrapers.freshersworld import FreshersworldScraper
from scrapers.timesjobs import TimesJobsScraper
from scrapers.foundit import FounditScraper
from scrapers.remoteok import RemoteOKScraper
from scrapers.remotive import RemotiveScraper
from scrapers.weworkremotely import WeWorkRemotelyScraper
from scrapers.jobspresso import JobspressoScraper
from scrapers.workingnomads import WorkingNomadsScraper
from scrapers.yc import YCScraper
from scrapers.wellfound import WellfoundScraper
from scrapers.otta import OttaScraper
from scrapers.reed import ReedScraper
from scrapers.cwjobs import CWJobsScraper
from scrapers.graduatejobs import GraduateJobsScraper
from scrapers.iamexpat import IamExpatScraper
from scrapers.undutchables import UndutchablesScraper

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobSearchAssistant:
    def __init__(self):
        self.skill_matcher = SkillMatcher(SKILLS_BASE)
        self.excel_writer = ExcelWriter()
        self.cover_letter_gen = CoverLetterGenerator()
        self.telegram = TelegramNotifier()
        self.db = JobDatabase()
        
        # Initialize all scrapers
        self.scrapers = [
            IndeedScraper(),
            NaukriScraper(),
            InstahyreScraper(),
            CutshortScraper(),
            FreshersworldScraper(),
            TimesJobsScraper(),
            FounditScraper(),
            RemoteOKScraper(),
            RemotiveScraper(),
            WeWorkRemotelyScraper(),
            JobspressoScraper(),
            WorkingNomadsScraper(),
            YCScraper(),
            WellfoundScraper(),
            OttaScraper(),
            ReedScraper(),
            CWJobsScraper(),
            GraduateJobsScraper(),
            IamExpatScraper(),
            UndutchablesScraper()
        ]
    
    async def scrape_all_jobs(self) -> List[Dict]:
        """Scrape jobs from all portals"""
        all_jobs = []
        
        logger.info(f"Starting job scraping from {len(self.scrapers)} portals...")
        
        for scraper in self.scrapers:
            try:
                logger.info(f"Scraping {scraper.name}...")
                jobs = await scraper.scrape()
                logger.info(f"Found {len(jobs)} jobs from {scraper.name}")
                all_jobs.extend(jobs)
            except Exception as e:
                logger.error(f"Error scraping {scraper.name}: {str(e)}")
                logger.debug(traceback.format_exc())
        
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        return all_jobs
    
    def filter_and_match_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter duplicates and match skills"""
        logger.info("Filtering duplicates and matching skills...")
        
        # Remove duplicates
        unique_jobs = self.db.filter_duplicates(jobs)
        logger.info(f"Unique jobs after deduplication: {len(unique_jobs)}")
        
        # Match skills
        matched_jobs = []
        for job in unique_jobs:
            matched_job = self.skill_matcher.match_job(job)
            if matched_job['match_percentage'] >= MIN_MATCH_PERCENTAGE:
                matched_jobs.append(matched_job)
        
        # Sort by match percentage
        matched_jobs.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        # Limit to max jobs
        matched_jobs = matched_jobs[:MAX_JOBS_PER_RUN]
        
        logger.info(f"Matched jobs above {MIN_MATCH_PERCENTAGE}%: {len(matched_jobs)}")
        return matched_jobs
    
    async def generate_cover_letters(self, jobs: List[Dict]) -> List[Dict]:
        """Generate cover letters for all jobs"""
        logger.info("Generating cover letters...")
        
        for job in jobs:
            try:
                cover_letter = await self.cover_letter_gen.generate(job)
                job['cover_letter_path'] = cover_letter
                job['cover_letter_generated'] = 'Yes'
            except Exception as e:
                logger.error(f"Error generating cover letter for {job.get('company', 'Unknown')}: {str(e)}")
                job['cover_letter_generated'] = 'No'
        
        return jobs
    
    async def run_morning_task(self):
        """Main morning task: scrape, match, generate"""
        try:
            logger.info("=" * 50)
            logger.info("Starting Morning Job Search Task")
            logger.info("=" * 50)
            
            # Scrape jobs
            all_jobs = await self.scrape_all_jobs()
            
            if not all_jobs:
                message = "⚠️ No jobs found from any portal. Please check scrapers."
                logger.warning(message)
                await self.telegram.send_message(message)
                return
            
            # Filter and match
            matched_jobs = self.filter_and_match_jobs(all_jobs)
            
            if not matched_jobs:
                message = "No jobs matched the skill criteria (>= 50%)."
                logger.info(message)
                await self.telegram.send_message(message)
                return
            
            # Generate cover letters
            matched_jobs = await self.generate_cover_letters(matched_jobs)
            
            # Generate Excel
            excel_path = self.excel_writer.write_jobs(matched_jobs)
            logger.info(f"Excel file generated: {excel_path}")
            
            # Save to history
            self.db.save_jobs(matched_jobs)
            
            # Send Telegram notification
            max_match = max(job['match_percentage'] for job in matched_jobs)
            message = f"""✅ Good Morning!

📊 {len(matched_jobs)} matched jobs found today.
🎯 Highest match: {max_match:.1f}%
📁 Excel generated: {excel_path}

💼 Keep applying and good luck!"""
            
            await self.telegram.send_message(message)
            
            logger.info("Morning task completed successfully!")
            logger.info("=" * 50)
            
        except Exception as e:
            error_msg = f"❌ Error in morning task: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            await self.telegram.send_message(error_msg)
    
    async def run_reminder_task(self):
        """Afternoon reminder task"""
        try:
            logger.info("Sending afternoon reminder...")
            
            # Get today's job count
            today_jobs = self.db.get_today_jobs_count()
            
            message = f"""⏰ Reminder!

You found {today_jobs} matched jobs today.
🎯 Target: Apply to at least 15 jobs.

💪 Keep going! Your dream job is waiting."""
            
            await self.telegram.send_message(message)
            logger.info("Reminder sent successfully!")
            
        except Exception as e:
            logger.error(f"Error in reminder task: {str(e)}")


async def main():
    """Main entry point"""
    assistant = JobSearchAssistant()
    
    if len(sys.argv) > 1:
        task = sys.argv[1]
        if task == "morning":
            await assistant.run_morning_task()
        elif task == "reminder":
            await assistant.run_reminder_task()
        else:
            print("Usage: python main.py [morning|reminder]")
    else:
        # Default: run morning task
        await assistant.run_morning_task()


if __name__ == "__main__":
    asyncio.run(main())
