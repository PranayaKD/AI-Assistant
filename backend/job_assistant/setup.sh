#!/bin/bash

# Setup script for AI Job Search Assistant

echo \"========================================\"
echo \"AI Job Search Assistant - Setup\"
echo \"========================================\"
echo \"\"

# Navigate to project directory
cd /app/backend/job_assistant

# Install Python dependencies
echo \"[1/4] Installing Python dependencies...\"
pip install -q -r requirements.txt
pip install -q emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

echo \"✓ Dependencies installed\"
echo \"\"

# Check .env file
echo \"[2/4] Checking environment configuration...\"
if [ -f \".env\" ]; then
    echo \"✓ .env file found\"
else
    echo \"⚠ .env file not found. Please create one with required credentials.\"
fi
echo \"\"

# Create output directories
echo \"[3/4] Creating output directories...\"
mkdir -p database output/excel output/coverletters
echo \"✓ Directories created\"
echo \"\"

# Display configuration status
echo \"[4/4] Configuration Status:\"
echo \"\"

if grep -q \"EMERGENT_LLM_KEY=sk-emergent\" .env; then
    echo \"✓ Emergent LLM Key configured\"
else
    echo \"⚠ Emergent LLM Key not configured\"
fi

if grep -q \"TELEGRAM_BOT_TOKEN=.\" .env && [ \"$(grep TELEGRAM_BOT_TOKEN .env | cut -d '=' -f2)\" != \"\" ]; then
    echo \"✓ Telegram Bot Token configured\"
else
    echo \"⚠ Telegram Bot Token not configured (optional but recommended)\"
fi

if grep -q \"TELEGRAM_CHAT_ID=.\" .env && [ \"$(grep TELEGRAM_CHAT_ID .env | cut -d '=' -f2)\" != \"\" ]; then
    echo \"✓ Telegram Chat ID configured\"
else
    echo \"⚠ Telegram Chat ID not configured (optional but recommended)\"
fi

echo \"\"
echo \"========================================\"
echo \"Setup Complete!\"
echo \"========================================\"
echo \"\"
echo \"Next steps:\"
echo \"1. Update your personal info in config.py\"
echo \"2. Set Telegram credentials in .env (optional)\"
echo \"3. Run: python main.py morning\"
echo \"\"
echo \"For full documentation, see README.md\"
echo \"\"
