# 🤖 AI Job Search Assistant

An AI-powered job search automation tool that scrapes multiple job portals, matches jobs to your skills, generates cover letters, and sends notifications — all running on **free tools**.

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=for-the-badge&logo=google)

---

## ✨ Features

- 🔍 **Multi-Portal Job Scraping** — Scrapes 20+ job portals (RemoteOK, Remotive, Indeed, Naukri, etc.)
- 🎯 **Skill Matching** — Automatically matches jobs against your skill set (50%–100% match filter)
- 📊 **Excel Reports** — Generates daily Excel files with formatted job listings
- 📝 **AI Cover Letters** — Auto-generates personalized cover letters using Google Gemini (free)
- 📱 **Telegram Notifications** — Sends daily job alerts via Telegram bot
- ⏰ **GitHub Actions Scheduler** — Automated daily runs at 9:00 AM & 2:15 PM IST
- 🚫 **Duplicate Prevention** — Tracks seen jobs to avoid duplicates
- 🖥️ **Dashboard UI** — Beautiful dark-themed React dashboard

---

## 🏗️ Project Structure

```
AI-Assistant/
├── backend/
│   ├── server.py                 # FastAPI server (API endpoints)
│   ├── requirements.txt          # Backend dependencies
│   ├── .env                      # Backend environment variables
│   └── job_assistant/
│       ├── main.py               # CLI entry point
│       ├── config.py             # Configuration & skills
│       ├── scrapers/             # 20+ job portal scrapers
│       ├── matcher/              # Skill matching engine
│       ├── generator/            # Excel & cover letter generators
│       ├── notifier/             # Telegram bot notifications
│       ├── database/             # JSON-based job history
│       └── output/               # Generated files (Excel, cover letters)
├── frontend/
│   ├── src/
│   │   ├── App.js                # Main dashboard component
│   │   ├── App.css               # Premium dark theme styles
│   │   └── components/ui/        # shadcn/ui components
│   ├── package.json
│   └── .env                      # Frontend environment variables
└── .github/workflows/
    └── job_scheduler.yml         # GitHub Actions automation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **MongoDB** (optional) — [Install](https://www.mongodb.com/try/download/community) or use [MongoDB Atlas Free](https://www.mongodb.com/atlas/database)

### Step 1: Clone the Repository

```bash
git clone https://github.com/PranayaKD/AI-Assistant.git
cd AI-Assistant
```

### Step 2: Set Up Backend

```bash
# Create Python virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment file
cp .env.example .env
# Edit .env with your MongoDB URL (or keep default for local)
```

### Step 3: Set Up Job Assistant

```bash
cd job_assistant

# Edit the .env file
# Add your Gemini API key (FREE): https://aistudio.google.com/apikey
# Optionally add Telegram bot credentials

# Edit config.py to update your personal information
```

### Step 4: Set Up Frontend

```bash
cd ../../frontend

# Install dependencies
yarn install
# OR
npm install
```

### Step 5: Run the Application

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn server:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
yarn start
# OR
npm start
```

**Visit:** [http://localhost:3000](http://localhost:3000)

---

## 🔑 API Keys Setup

### Google Gemini (FREE — for AI cover letters)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Add to `backend/job_assistant/.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

### Telegram Bot (Optional — for notifications)

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot and get the token
3. Message [@userinfobot](https://t.me/userinfobot) to get your Chat ID
4. Add to `backend/job_assistant/.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

---

## ⚙️ GitHub Actions (Automated Daily Runs)

To enable automated job searching via GitHub Actions:

1. Go to your repo → **Settings** → **Secrets and Variables** → **Actions**
2. Add these secrets:
   - `GEMINI_API_KEY` — Your Google Gemini API key
   - `TELEGRAM_BOT_TOKEN` — Your Telegram bot token (optional)
   - `TELEGRAM_CHAT_ID` — Your Telegram chat ID (optional)
3. The workflow runs automatically:
   - **9:00 AM IST** — Morning job search
   - **2:15 PM IST** — Afternoon reminder
4. You can also trigger manually from the **Actions** tab

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | Health check |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/jobs` | All scraped & matched jobs |
| POST | `/api/search` | Trigger a new job search |
| GET | `/api/cover-letters` | List generated cover letters |
| GET | `/api/cover-letters/{filename}` | Get specific cover letter |
| GET | `/api/health` | Detailed health status |

**Interactive API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ Running the Job Search CLI

You can also run the job assistant directly:

```bash
cd backend/job_assistant

# Run morning job search
python main.py morning

# Run afternoon reminder
python main.py reminder
```

---

## 📋 Configuration

Edit `backend/job_assistant/config.py` to customize:

- **PERSONAL_INFO** — Your name, email, GitHub, LinkedIn
- **SKILLS_BASE** — Your skills for job matching
- **TARGET_LOCATIONS** — Preferred job locations
- **JOB_TITLES** — Target job titles to search
- **MIN_MATCH_PERCENTAGE** — Minimum skill match % (default: 50%)
- **MAX_JOBS_PER_RUN** — Maximum jobs per run (default: 35)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Pranaya KD**
- GitHub: [@PranayaKD](https://github.com/PranayaKD)
