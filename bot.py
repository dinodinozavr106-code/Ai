import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent?key=" + GEMINI_KEY
    body = {"contents": [{"parts": [{"text": user_text}]}]}
    r = requests.post(url, json=body)
    data = r.json()
    if "candidates" in data:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        answer = str(data)
    await update.message.reply_text(answer)

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling(drop_pending_updates=True)
