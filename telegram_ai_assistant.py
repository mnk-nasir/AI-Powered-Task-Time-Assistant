#!/usr/bin/env python3
"""
Telegram AI Assistant
---------------------
Rebuild of the n8n "Telegram AI Assistant" workflow in Python.

Features:
- Listens to incoming Telegram messages (text or voice)
- Converts voice to text (mocked OpenAI speech-to-text)
- Sends user text to OpenAI model (mock GPT-style response)
- Optionally fetches Google Calendar or Gmail messages (mocked)
- Replies back to the user in Telegram chat

Author: Converted automatically from n8n workflow JSON
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from openai import OpenAI
from config import Config
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("telegram_ai_assistant")

cfg = Config.load_from_env()

# --- Mock integrations (replace with real API calls later) ---
def mock_google_calendar():
    log.info("[Mock Google Calendar] Returning 2 sample events.")
    return [
        {"summary": "Team meeting", "start": {"dateTime": "2025-10-25T10:00:00"}},
        {"summary": "Lunch with client", "start": {"dateTime": "2025-10-25T13:00:00"}},
    ]

def mock_gmail():
    log.info("[Mock Gmail] Returning 2 sample emails.")
    return [
        {"sender": "alice@example.com", "subject": "Meeting follow-up", "snippet": "Thanks for your time today..."},
        {"sender": "bob@example.com", "subject": "New project", "snippet": "Please see attached proposal..."},
    ]

def mock_baserow_tasks():
    return [{"task": "Finish report", "due": "2025-10-26"}]


# --- OpenAI Assistant (mocked if no key) ---
async def ai_generate_response(user_text: str) -> str:
    if cfg.mock:
        return f"🤖 [Mock AI] You said: '{user_text}'. Here's what I think: sounds interesting!"
    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant integrated with Telegram."},
            {"role": "user", "content": user_text}
        ]
    )
    return completion.choices[0].message.content


# --- Telegram Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I’m your AI Assistant. Send me a message or voice note to get started.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if not text:
        await update.message.reply_text("I didn’t receive any text. Try sending a message or voice.")
        return

    log.info(f"Message from @{update.message.from_user.username}: {text}")
    response = await ai_generate_response(text)
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    log.info(f"Received voice message from {user.username or user.id}")

    # Download voice note (mock transcription)
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = f"voice_{user.id}.ogg"
    await file.download_to_drive(file_path)
    log.info(f"Downloaded voice note to {file_path}")

    # Mock speech-to-text
    transcript = "[Mock transcription] User said something via voice."
    log.info(f"Transcript: {transcript}")

    # Generate AI response
    ai_reply = await ai_generate_response(transcript)
    await update.message.reply_text(ai_reply)

    # Clean up
    try:
        os.remove(file_path)
    except Exception:
        pass


# --- Main Entry Point ---
def main():
    if not cfg.TELEGRAM_BOT_TOKEN:
        log.error("Missing TELEGRAM_BOT_TOKEN in environment. Exiting.")
        return

    app = ApplicationBuilder().token(cfg.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    log.info("🤖 Telegram AI Assistant is running...")
    app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
