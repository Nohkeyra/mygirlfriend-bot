import os
import logging
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("No TELEGRAM_BOT_TOKEN set!")
    exit(1)

# Flask app for health checks (required by Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/healthz')
def health():
    return "OK"

# Telegram bot handlers
async def start(update: Update, context):
    await update.message.reply_text("🌸 Hello! I'm your AI girlfriend!\nSend me a message and I'll reply.")

async def echo(update: Update, context):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

def run_bot():
    """Run the bot in a separate thread with its own event loop"""
    logger.info("Starting bot thread...")
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Build the application
        telegram_app = Application.builder().token(TOKEN).build()
        
        # Add handlers
        telegram_app.add_handler(CommandHandler("start", start))
        telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        logger.info("Bot polling started")
        # Run polling WITHOUT signal handlers (fixes the thread error)
        telegram_app.run_polling(stop_signals=None)
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)

# Start the bot in a background thread when Flask starts
thread = threading.Thread(target=run_bot, daemon=True)
thread.start()
logger.info("Bot thread started")

if __name__ == "__main__":
    # Get port from environment (Render provides PORT)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
