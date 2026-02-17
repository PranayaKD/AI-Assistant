# 🎓 COMPLETE SETUP & DEPLOYMENT GUIDE

## Table of Contents
1. [Local Setup & Testing](#local-setup--testing)
2. [GitHub Actions Deployment](#github-actions-deployment)
3. [Telegram Bot Setup](#telegram-bot-setup)
4. [Daily Workflow](#daily-workflow)
5. [Troubleshooting](#troubleshooting)

---

## 1. Local Setup & Testing

### Step 1: Install Dependencies

```bash
cd /app/backend/job_assistant

# Install Python packages
pip install -r requirements.txt

# Install Emergent integrations (for AI cover letters)
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

**Expected output:**
```
Successfully installed aiohttp, beautifulsoup4, openpyxl, python-dotenv, emergentintegrations...
```

---

### Step 2: Configure Personal Information

Edit `config.py` and update the `PERSONAL_INFO` section:

```python
PERSONAL_INFO = {
    "name": "Your Full Name",           # Replace with your name
    "email": "your.email@example.com",  # Your email
    "phone": "+91-XXXXXXXXXX",          # Your phone
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "portfolio": "https://yourportfolio.com"
}
```

**Also review and adjust:**
- `SKILLS_BASE` - Add your specific skills
- `MAX_JOBS_PER_RUN` - Default: 35
- `MIN_MATCH_PERCENTAGE` - Default: 50%

---

### Step 3: Test Components

```bash
# Quick test to verify everything works
python test_components.py
```

**Expected output:**
```
[1/3] Testing Skill Matcher...
  ✓ Matched skills: django, postgresql, python, rest apis
  ✓ Match percentage: 100.0%

[2/3] Testing Remote OK Scraper...
  ✓ Successfully scraped X jobs

[3/3] Testing Excel Writer...
  ✓ Excel created: /app/backend/job_assistant/output/excel/Jobs_17_02_2026.xlsx

✅ All Components Working!
```

---

### Step 4: Run Your First Job Search

```bash
# Run morning task (full job search)
python main.py morning
```

This will:
1. ✅ Scrape jobs from 20+ portals
2. ✅ Filter for skill matches (≥50%)
3. ✅ Generate Excel file
4. ✅ Create AI cover letters
5. ✅ Send Telegram notification (if configured)

**Check results:**
```bash
ls -lh output/excel/
ls -lh output/coverletters/
```

---

## 2. GitHub Actions Deployment

Deploy to GitHub for **free automated daily runs**!

### Step 1: Create GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Job Search Assistant"

# Create repository on GitHub (via web interface)
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/job-search-assistant.git
git branch -M main
git push -u origin main
```

---

### Step 2: Configure Repository Secrets

Go to your GitHub repository:

1. Click **Settings** tab
2. Navigate to **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these 3 secrets:

| Secret Name | Value | Where to get it |
|-------------|-------|-----------------|
| `EMERGENT_LLM_KEY` | `sk-emergent-7Ad791dAc7bA87e088` | Already provided |
| `TELEGRAM_BOT_TOKEN` | Your bot token | See Step 3 below |
| `TELEGRAM_CHAT_ID` | Your chat ID | See Step 3 below |

**For each secret:**
- Click "New repository secret"
- Enter Name (exactly as shown above)
- Enter Value
- Click "Add secret"

---

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. You'll see "Job Search Assistant Scheduler" workflow
3. If prompted, click **"I understand my workflows, go ahead and enable them"**

The workflow will now run automatically:
- **9:00 AM IST** (3:30 UTC) - Morning job search
- **2:15 PM IST** (8:45 UTC) - Reminder notification

---

### Step 4: Manual Test Run

Before waiting for the schedule:

1. Go to **Actions** tab
2. Click **"Job Search Assistant Scheduler"** workflow
3. Click **"Run workflow"** dropdown (right side)
4. Click **"Run workflow"** button

Wait 2-3 minutes for completion.

---

### Step 5: Download Results

After workflow completes:

1. Go to **Actions** tab
2. Click on the completed workflow run (green checkmark)
3. Scroll down to **Artifacts** section
4. Download:
   - `job-applications` (Excel file)
   - `cover-letters` (Text files)

---

## 3. Telegram Bot Setup

Get notifications on your phone!

### Step 1: Create Telegram Bot

1. Open **Telegram** app
2. Search for **@BotFather**
3. Start a chat
4. Send: `/newbot`
5. Follow prompts:
   - **Bot name**: "My Job Search Bot" (or any name)
   - **Bot username**: "myjobsearch_bot" (must be unique, ends with 'bot')

6. **Copy the token** (looks like):
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

---

### Step 2: Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Send any message to it
3. It will reply with your user info
4. **Copy your ID** (looks like):
   ```
   123456789
   ```

---

### Step 3: Start Conversation with Your Bot

1. Search for your bot username (e.g., @myjobsearch_bot)
2. Click on it
3. Click **"Start"** button
4. This is required for bot to send you messages!

---

### Step 4: Add Credentials

**For Local Use:**
Edit `.env` file:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

**For GitHub Actions:**
Add as repository secrets (see Step 2 of GitHub deployment)

---

### Step 5: Test Telegram

```bash
python main.py reminder
```

You should receive a test message on Telegram!

---

## 4. Daily Workflow

### Morning (9:00 AM IST)

**Automated (GitHub Actions):**
- Job search runs automatically
- Receives Telegram notification
- Downloads artifacts from GitHub

**Manual (Local):**
```bash
python main.py morning
```

**What you do:**
1. Check Telegram notification (summary of jobs found)
2. Open Excel file from `output/excel/`
3. Review matched jobs sorted by percentage
4. Open relevant cover letters from `output/coverletters/`

---

### Throughout the Day

**Applying to Jobs:**
1. Customize cover letter for each application
2. Update Excel columns:
   - **Status**: "Applied", "Pending", "Rejected", "Interview"
   - **Mail Sent**: "Yes"
   - **Interview Date**: If scheduled
   - **Remarks**: Any notes

---

### Afternoon (2:15 PM IST)

**Automated:**
- Receives reminder notification
- Shows count of jobs found today
- Encourages hitting daily target (15+ applications)

---

### Weekly Review

1. Review Excel file for:
   - Response rate
   - Most responsive portals
   - Common missing skills
2. Update `SKILLS_BASE` in config.py if needed
3. Adjust `MIN_MATCH_PERCENTAGE` based on results

---

## 5. Troubleshooting

### Issue: "No jobs found"

**Causes:**
- Some portals may be temporarily unavailable
- Google search rate limiting
- Network connectivity issues

**Solutions:**
```bash
# Wait 30 minutes and try again
python main.py morning

# Check specific scraper
python -c "
import asyncio
from scrapers.remoteok import RemoteOKScraper
async def test():
    scraper = RemoteOKScraper()
    jobs = await scraper.scrape()
    print(f'Found {len(jobs)} jobs')
asyncio.run(test())
"
```

---

### Issue: "Telegram not working"

**Causes:**
- Bot token/chat ID incorrect
- Haven't started conversation with bot
- Network issues

**Solutions:**
```bash
# Test bot token
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"

# Expected response: {"ok":true,"result":{...}}

# Test sending message
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
  -d "chat_id=<YOUR_CHAT_ID>&text=Test"
```

**Common mistakes:**
- ❌ Forgot to click "Start" on bot
- ❌ Wrong chat ID format (should be numbers only)
- ❌ Extra spaces in token/ID

---

### Issue: "Cover letter generation fails"

**Causes:**
- EMERGENT_LLM_KEY not configured
- emergentintegrations not installed
- Network/API issues

**Solutions:**
```bash
# Check key is set
cat .env | grep EMERGENT_LLM_KEY

# Should show: EMERGENT_LLM_KEY=sk-emergent-...

# Test emergentintegrations
python -c "
from emergentintegrations.llm.chat import LlmChat
print('✓ emergentintegrations working')
"

# Reinstall if needed
pip install -U emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

---

### Issue: "GitHub Actions failing"

**Causes:**
- Secrets not set correctly
- Workflow file syntax error
- Python dependency issues

**Solutions:**

1. **Check secrets are set:**
   - Settings → Secrets → Actions
   - Verify all 3 secrets exist

2. **Check workflow logs:**
   - Actions → Failed workflow → Click on job
   - Read error messages

3. **Common fixes:**
   ```yaml
   # If Python version issue, update workflow:
   - uses: actions/setup-python@v4
     with:
       python-version: '3.11'  # or '3.12'
   ```

---

### Issue: "Excel file not opening"

**Causes:**
- Corrupted file
- Missing openpyxl

**Solutions:**
```bash
# Reinstall openpyxl
pip install -U openpyxl

# Test Excel generation
python -c "
from generator.excel_writer import ExcelWriter
writer = ExcelWriter()
test_job = {
    'job_id': 'TEST', 'company': 'Test Co', 'title': 'Dev',
    'link': 'http://test.com', 'portal': 'Test',
    'required_skills': ['Python'], 'matched_skills': ['Python'],
    'missing_skills': [], 'match_percentage': 100,
    'cover_letter_generated': 'Yes'
}
path = writer.write_jobs([test_job])
print(f'✓ Excel created: {path}')
"
```

---

### Issue: "Some scrapers return 0 jobs"

**This is normal!**

**Reasons:**
- Not all portals have Python jobs every day
- Google search rate limits
- Portal-specific issues

**Expected behavior:**
- 15-20 scrapers return results
- 3-5 might return 0 jobs
- Total 30-35 jobs is still achieved

**Not a problem unless ALL scrapers return 0 jobs.**

---

### Debug Mode

Enable detailed logging:

```bash
# In .env file
LOG_LEVEL=DEBUG

# Run with verbose output
python main.py morning 2>&1 | tee job_search.log

# Check log file
cat job_search.log
```

---

## 🎯 Success Checklist

Before considering setup complete:

- [ ] Installed all dependencies without errors
- [ ] Updated personal info in config.py
- [ ] Ran test_components.py successfully
- [ ] Ran first job search (python main.py morning)
- [ ] Excel file generated in output/excel/
- [ ] Cover letters generated in output/coverletters/
- [ ] Telegram bot created (if using notifications)
- [ ] Telegram notifications working (if configured)
- [ ] GitHub repository created (if using automation)
- [ ] GitHub secrets configured (if using automation)
- [ ] GitHub Actions workflow enabled (if using automation)
- [ ] Manual workflow run successful (if using automation)

---

## 🆘 Getting Help

If you're still stuck after troubleshooting:

1. **Check logs:**
   ```bash
   python main.py morning 2>&1 | tee debug.log
   cat debug.log
   ```

2. **Verify environment:**
   ```bash
   python --version  # Should be 3.11+
   pip list | grep -E "aiohttp|beautifulsoup4|openpyxl|emergent"
   ```

3. **Test individual components:**
   ```bash
   python test_components.py
   ```

4. **Check file permissions:**
   ```bash
   ls -la output/
   ls -la database/
   ```

---

## 🎉 You're All Set!

Your AI Job Search Assistant is now fully configured and ready to use!

**Quick command reference:**
```bash
# Full job search
python main.py morning

# Reminder only
python main.py reminder

# Test components
python test_components.py

# Check results
ls output/excel/
ls output/coverletters/
```

**Happy job hunting! 🚀**
