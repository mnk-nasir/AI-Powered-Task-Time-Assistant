# AI-Powered-Task-Time-Assistant
The current version includes placeholders for:  Google Calendar → mock_google_calendar()  Gmail → mock_gmail()  Baserow → mock_baserow_tasks()  To make them real, replace those functions with API calls using official SDKs.
# Telegram AI Assistant 🤖

Python-based automation that replicates your n8n workflow for an AI-powered Telegram Assistant.

---

## 🧠 Features
- Responds to Telegram text and voice messages
- Uses OpenAI GPT model for conversation (mocked if no key)
- Optional integrations for Gmail, Google Calendar, and Baserow (mocked)
- Fully runnable in **mock mode** without any API keys

---

## 🚀 Quick Start

1. Clone this project and enter the folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create .env:

bash
Copy code
cp .env.example .env
Fill in TELEGRAM_BOT_TOKEN from @BotFather

If you don’t have any keys, leave everything blank (mock mode auto-enabled)

Run the bot:

bash
Copy code
python telegram_ai_assistant.py
🧩 Extending the Bot
The current version includes placeholders for:

Google Calendar → mock_google_calendar()

Gmail → mock_gmail()

Baserow → mock_baserow_tasks()

To make them real, replace those functions with API calls using official SDKs.

🕓 Deploying
You can deploy this on:

Local PC or Raspberry Pi

A small VPS (using systemd or Docker)

GitHub Actions or Render cron jobs for background operation

