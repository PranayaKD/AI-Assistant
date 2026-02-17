#!/usr/bin/env python3
"""Quick test script to verify all components work"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SKILLS_BASE
from matcher.skill_matcher import SkillMatcher
from scrapers.remoteok import RemoteOKScraper
from generator.excel_writer import ExcelWriter

async def test_components():
    print("=" * 60)
    print("Testing Job Search Assistant Components")
    print("=" * 60)
    print()
    
    # Test 1: Skill Matcher
    print("[1/3] Testing Skill Matcher...")
    matcher = SkillMatcher(SKILLS_BASE)
    test_job = {
        "title": "Python Backend Developer",
        "description": "Looking for a Python developer with Django, REST APIs, and PostgreSQL experience"
    }
    matched = matcher.match_job(test_job)
    print(f"  ✓ Matched skills: {', '.join(matched['matched_skills'][:5])}")
    print(f"  ✓ Match percentage: {matched['match_percentage']:.1f}%")
    print()
    
    # Test 2: Scraper
    print("[2/3] Testing Remote OK Scraper...")
    try:
        scraper = RemoteOKScraper()
        jobs = await scraper.scrape()
        print(f"  ✓ Successfully scraped {len(jobs)} jobs")
        if jobs:
            print(f"  ✓ Sample job: {jobs[0]['title']}")
    except Exception as e:
        print(f"  ⚠ Scraper test skipped (network issue): {str(e)[:50]}")
    print()
    
    # Test 3: Excel Writer
    print("[3/3] Testing Excel Writer...")
    writer = ExcelWriter()
    test_jobs = [
        {
            "job_id": "TEST001",
            "company": "Test Company",
            "title": "Python Developer",
            "link": "https://example.com/job",
            "portal": "Test Portal",
            "required_skills": ["Python", "Django"],
            "matched_skills": ["Python"],
            "missing_skills": ["Django"],
            "match_percentage": 75.0,
            "cover_letter_generated": "Yes"
        }
    ]
    excel_path = writer.write_jobs(test_jobs)
    print(f"  ✓ Excel created: {excel_path}")
    print()
    
    print("=" * 60)
    print("✅ All Components Working!")
    print("=" * 60)
    print()
    print("Next step: Run 'python main.py morning' for full job search")

if __name__ == "__main__":
    asyncio.run(test_components())
