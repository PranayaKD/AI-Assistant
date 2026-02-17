# Quick Start Guide

## 🚀 Fastest Way to Get Started

### 1. Install Dependencies (30 seconds)

```bash
cd /app/backend/job_assistant
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### 2. Configure Your Details (2 minutes)

Edit `config.py` and update:

```python
PERSONAL_INFO = {
    "name": "YOUR NAME HERE",
    "email": "your.email@example.com",
    "phone": "+91-XXXXXXXXXX",
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "portfolio": "https://yourportfolio.com"
}
```

### 3. Run Your First Job Search! (Instant)

```bash
python main.py morning
```

**That's it!** Check the output folder for your Excel file and cover letters.

---

## 📱 Add Telegram Notifications (Optional - 3 minutes)

### Step 1: Create Bot
1. Open Telegram, search for `@BotFather`
2. Send: `/newbot`
3. Choose a name (e.g., "My Job Search Bot")
4. Choose a username (e.g., "myjobsearch_bot")
5. Copy the **token** (looks like: `123456:ABC-DEF...`)

### Step 2: Get Your Chat ID
1. Search for `@userinfobot` on Telegram
2. Send any message
3. Copy your **ID** (looks like: `123456789`)

### Step 3: Add to .env
Edit `.env` file:
```env
TELEGRAM_BOT_TOKEN=paste_your_token_here
TELEGRAM_CHAT_ID=paste_your_chat_id_here
```

### Step 4: Start conversation with your bot
1. Search for your bot username on Telegram
2. Click "Start" button
3. Now you'll receive notifications!

---

## 📊 Understanding the Output

### Excel File
Location: `output/excel/Jobs_DD_MM_YYYY.xlsx`

The Excel contains:
- ✅ **Auto-filled**: Job details, skills, match %, resume changes needed
- ✏️ **Manual tracking**: Status, interview dates, mail sent, responses

### Cover Letters
Location: `output/coverletters/`

Each job gets a personalized 150-200 word cover letter.

---

## 🤖 Deploy to GitHub Actions (Free Automation)

### One-Time Setup (5 minutes)

1. **Create GitHub Repository**
   - Go to github.com
   - Create new repository
   - Push this code

2. **Add Secrets**
   - Repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add these 3 secrets:

   | Name | Value |
   |------|-------|
   | `EMERGENT_LLM_KEY` | `sk-emergent-7Ad791dAc7bA87e088` |
   | `TELEGRAM_BOT_TOKEN` | Your bot token |
   | `TELEGRAM_CHAT_ID` | Your chat ID |

3. **Enable Actions**
   - Go to Actions tab
   - Enable workflows
   - Done! It runs automatically at 9 AM & 2:15 PM IST daily

4. **Download Results**
   - After workflow runs, go to Actions
   - Click the completed run
   - Download "job-applications" and "cover-letters" artifacts

---

## 🎯 What Happens Automatically?

### Every Day at 9:00 AM IST:
1. ✅ Scrapes 30-35 jobs from 20+ portals
2. ✅ Filters for 50%+ skill match
3. ✅ Generates Excel tracking sheet
4. ✅ Creates AI cover letters
5. ✅ Sends Telegram summary

### Every Day at 2:15 PM IST:
1. ✅ Sends reminder to apply
2. ✅ Shows daily job count

---

## ⚙️ Customize Your Search

### Add More Skills
Edit `config.py`:
```python
SKILLS_BASE = [
    "Python", "Django", "FastAPI",
    "Add", "Your", "Skills"
]
```

### Change Targets
```python
MAX_JOBS_PER_RUN = 35  # More or fewer jobs
MIN_MATCH_PERCENTAGE = 50  # Stricter/looser matching
```

### Change Schedule
Edit `.github/workflows/job_scheduler.yml`:
```yaml
- cron: '30 3 * * *'  # Change time (in UTC)
```

---

## 🔧 Troubleshooting

### "No jobs found"
- Normal! Some portals may be down temporarily
- Try running again in 30 minutes
- Google search has rate limits

### "Telegram not working"
- Did you start a chat with your bot?
- Double-check token and chat ID
- Try sending test: `curl "https://api.telegram.org/bot<TOKEN>/getMe"`

### "Cover letter error"
- Verify EMERGENT_LLM_KEY is in .env
- Check internet connection
- Ensure emergentintegrations is installed

---

## 📝 Daily Workflow Suggestion

1. **Morning (9:05 AM)**: Check Telegram notification
2. **Morning (9:15 AM)**: Review Excel file, filter top matches
3. **Morning-Afternoon**: Customize cover letters, apply to jobs
4. **Afternoon (2:15 PM)**: Get reminder, ensure you applied to 15+
5. **Evening**: Track responses in Excel manual columns

---

## 💡 Pro Tips

1. **Update Personal Info**: Keep config.py current with latest skills
2. **Customize Cover Letters**: Use generated letters as base, personalize
3. **Track Everything**: Use Excel manual columns religiously
4. **Set Daily Goals**: Target 15-20 applications/day
5. **Follow Up**: Mark follow-ups in Excel, set reminders

---

## 📈 Expected Results

- **30-35 jobs** matched daily
- **50-100%** skill match rate
- **20+ portals** coverage
- **Zero duplicates** (automatic tracking)
- **Personalized cover letters** for each job

---

## 🎉 You're All Set!

Run your first search:
```bash
python main.py morning
```

Then check:
- `output/excel/` for your tracking spreadsheet
- `output/coverletters/` for personalized letters
- Telegram for instant notification

**Good luck with your job search! 🚀**

---

## 📞 Need Help?

Check the full README.md for detailed documentation and troubleshooting.
