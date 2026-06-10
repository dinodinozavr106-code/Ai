import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CLAUDE_KEY = os.environ.get("CLAUDE_KEY")

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": user_text}]
    }
    r = requests.post(url, headers=headers, json=body)
    data = r.json()
    if "content" in data:
        answer = data["content"][0]["text"]
    else:
        answer = str(data)
    await update.message.reply_text(answer)

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling(drop_pending_updates=True)
