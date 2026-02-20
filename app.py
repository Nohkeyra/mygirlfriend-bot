import os
import asyncio
import threading
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Create FastAPI app (to keep Hugging Face happy)
app = FastAPI()

# Get token from environment variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Telegram bot handlers
async def start(update: Update, context):
    await update.message.reply_text(
        "🌸 Hello! I'm your AI girlfriend!\n"
        "Send me a message and I'll reply."
    )

async def echo(update: Update, context):
    user_message = update.message.text
    await update.message.reply_text(
        f"💬 You said: {user_message}\n\n"
        f"🤖 I'm thinking... (AI will reply here soon!)"
    )

# FastAPI endpoint (required by Hugging Face)
@app.get("/")
def home():
    return {"status": "Telegram bot is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Function to run Telegram bot in background
def run_bot():
    """Start the Telegram bot"""
    # Create the Application
    telegram_app = Application.builder().token(TOKEN).build()
    
    # Register handlers
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Start the bot
    print("🤖 Telegram bot is starting...")
    telegram_app.run_polling()

# Start bot in background when FastAPI starts
@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    print("✅ Bot thread started")

# For local testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
