# AI Job Search Automation Assistant

A complete production-ready automation system that finds, matches, and tracks Python/Django backend developer jobs daily from 20+ job portals.

## Features

- **Automated Daily Job Search**: Scrapes 30-35 relevant jobs every morning
- **Smart Skill Matching**: Filters jobs with 50-100% skill match
- **Excel Reports**: Generates detailed tracking spreadsheet
- **AI Cover Letters**: Creates personalized cover letters using GPT-4o
- **Telegram Notifications**: Morning summaries and afternoon reminders
- **Deduplication**: Tracks job history to avoid duplicates
- **20+ Job Portals**: Indeed, Naukri, Remote OK, Y Combinator, and more

## Job Portals Covered

### India
- Naukri
- Instahyre
- Cutshort
- Freshersworld
- TimesJobs
- Foundit

### Global
- Indeed
- Glassdoor
- Monster

### Remote
- Remote OK
- Remotive
- We Work Remotely
- Jobspresso
- Working Nomads

### Startup
- Y Combinator
- Wellfound (AngelList)
- Otta

### UK
- Reed.co.uk
- CWJobs
- GraduateJobs

### Netherlands
- IamExpat Jobs
- Undutchables

## Installation

### Local Setup

1. **Clone and Navigate**
```bash
cd /app/backend/job_assistant
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

3. **Configure Environment Variables**

Create a `.env` file in the `job_assistant` directory:

```env
# AI for Cover Letters (Already provided via Emergent)
EMERGENT_LLM_KEY=sk-emergent-7Ad791dAc7bA87e088

# Telegram Notifications
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional
LOG_LEVEL=INFO
```

### Getting Telegram Credentials

1. **Create Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the **Bot Token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
   - Set as `TELEGRAM_BOT_TOKEN`

2. **Get Your Chat ID**:
   - Search for `@userinfobot` on Telegram
   - Send any message
   - Copy your **Chat ID** (looks like: `123456789`)
   - Set as `TELEGRAM_CHAT_ID`

### Personal Configuration

Edit `/app/backend/job_assistant/config.py`:

```python
PERSONAL_INFO = {
    "name": "Your Full Name",
    "email": "your.email@example.com",
    "phone": "+91-XXXXXXXXXX",
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "portfolio": "https://yourportfolio.com"
}
```

## Usage

### Run Locally

```bash
cd /app/backend/job_assistant

# Morning task (scrape jobs, generate Excel, cover letters)
python main.py morning

# Reminder task (afternoon notification)
python main.py reminder

# Default (runs morning task)
python main.py
```

### Output Files

After running, find your files in:
- **Excel**: `/app/backend/job_assistant/output/excel/Jobs_DD_MM_YYYY.xlsx`
- **Cover Letters**: `/app/backend/job_assistant/output/coverletters/`
- **Job History**: `/app/backend/job_assistant/database/jobs_history.json`

## GitHub Actions Deployment (Free & Automated)

Run automatically every day on GitHub's free tier!

### Setup Steps

1. **Fork/Push to GitHub**
   - Create a new repository on GitHub
   - Push this code to your repository

2. **Set Repository Secrets**
   - Go to: `Settings` → `Secrets and variables` → `Actions`
   - Add these secrets:
     - `EMERGENT_LLM_KEY`: `sk-emergent-7Ad791dAc7bA87e088`
     - `TELEGRAM_BOT_TOKEN`: Your bot token
     - `TELEGRAM_CHAT_ID`: Your chat ID

3. **Enable GitHub Actions**
   - Go to `Actions` tab in your repository
   - Enable workflows if prompted
   - The workflow will run automatically at:
     - **9:00 AM IST** (3:30 UTC) - Morning job search
     - **2:15 PM IST** (8:45 UTC) - Reminder notification

4. **Manual Trigger**
   - Go to `Actions` → `Job Search Assistant Scheduler`
   - Click `Run workflow` to test immediately

5. **Download Results**
   - After workflow runs, go to `Actions`
   - Click on the completed workflow run
   - Download artifacts:
     - `job-applications` (Excel files)
     - `cover-letters` (Cover letter text files)

## Excel Report Structure

Generated file: `Jobs_DD_MM_YYYY.xlsx`

Auto-filled columns:
- S.No, Date, Job ID
- Company Name, Job Role, Job Link
- Job Portal, Exact Skills Required
- Match %, Resume Changes Needed
- Cover Letter Generated

Manual tracking columns:
- Status, Interview Mode, Interview Date
- Mail Sent, Cold Email Sent, Follow Up Mail
- Response Received, Remarks/Notes

## Architecture

```
job_assistant/
├── scrapers/          # 20 portal scrapers
├── matcher/           # Skill matching logic
├── generator/         # Excel & cover letter generation
├── notifier/          # Telegram notifications
├── database/          # Job history tracking
├── output/            # Excel & cover letters
├── config.py          # Configuration
└── main.py           # Main orchestrator
```

## Customization

### Add More Skills

Edit `SKILLS_BASE` in `config.py`:
```python
SKILLS_BASE = [
    "Python", "Django", "FastAPI",
    "Your", "Custom", "Skills"
]
```

### Change Job Limits

Edit in `config.py`:
```python
MAX_JOBS_PER_RUN = 35  # Total jobs
MIN_MATCH_PERCENTAGE = 50  # Minimum match %
JOBS_PER_PORTAL = 5  # Per portal limit
```

### Modify Schedule

Edit `.github/workflows/job_scheduler.yml`:
```yaml
schedule:
  - cron: '30 3 * * *'  # Your preferred time (UTC)
```

## Troubleshooting

### No jobs found
- Some portals may be temporarily unavailable
- Google search scraping may have rate limits
- Try running again after some time

### Telegram not working
- Verify bot token and chat ID are correct
- Make sure you've started a conversation with your bot
- Check bot has permission to send messages

### Cover letter generation fails
- Ensure EMERGENT_LLM_KEY is set correctly
- Check internet connection
- Verify emergentintegrations is installed

### GitHub Actions failing
- Check if secrets are set correctly
- Verify Python version compatibility
- Review workflow logs for specific errors

## Cost

- **Completely Free** when using:
  - GitHub Actions (2,000 free minutes/month)
  - Emergent LLM Key (provided, with usage limits)
  - Telegram Bot (free)

## Support

For issues or improvements, check the logs:
```bash
python main.py morning 2>&1 | tee job_search.log
```

## License

MIT License - Feel free to use and modify for your job search!
