import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("No TELEGRAM_BOT_TOKEN set!")
    exit(1)

# Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/healthz')
def health():
    return "OK"

# Telegram bot handlers
async def start(update: Update, context):
    await update.message.reply_text("🌸 Hello! I'm your AI girlfriend!")

async def echo(update: Update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

def run_bot():
    """Run the bot in a separate thread"""
    logger.info("Starting bot thread...")
    try:
        telegram_app = Application.builder().token(TOKEN).build()
        telegram_app.add_handler(CommandHandler("start", start))
        telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        logger.info("Bot polling started")
        telegram_app.run_polling()
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)

# Start bot in background thread when Flask starts
thread = threading.Thread(target=run_bot, daemon=True)
thread.start()
logger.info("Bot thread started")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
