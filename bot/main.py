import asyncio
import logging
import os
import sys
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
NGROK_API_URL = os.getenv("NGROK_API_URL", "http://ngrok:4040/api/tunnels")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set")
    sys.exit(1)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Global variable to store the current Ngrok URL
current_ngrok_url = None

async def fetch_ngrok_url():
    """Fetches the public HTTPS URL from the Ngrok API."""
    global current_ngrok_url
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(NGROK_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    tunnels = data.get("tunnels", [])
                    for tunnel in tunnels:
                        if tunnel.get("proto") == "https":
                            public_url = tunnel.get("public_url")
                            logger.info(f"Found Ngrok URL: {public_url}")
                            current_ngrok_url = public_url
                            return public_url
    except Exception as e:
        logger.error(f"Error fetching Ngrok URL: {e}")
    return None

async def monitor_ngrok_url():
    """Periodically checks for Ngrok URL updates."""
    global current_ngrok_url
    while True:
        url = await fetch_ngrok_url()
        if url and url != current_ngrok_url:
            current_ngrok_url = url
            logger.info(f"Updated Ngrok URL: {current_ngrok_url}")
        elif not url:
            logger.warning("Could not fetch Ngrok URL, retrying in 5 seconds...")
        await asyncio.sleep(10)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handler for the /start command."""
    if not current_ngrok_url:
        await message.answer("System is starting up, please try again in a moment...")
        # Try to fetch immediately
        await fetch_ngrok_url()
        return

    web_app_url = current_ngrok_url
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Open Web App", web_app={ "url": web_app_url })]
    ])
    
    await message.answer(
        f"Welcome! Click the button below to open the Web App.\nURL: {web_app_url}",
        reply_markup=keyboard
    )

async def main():
    # Start the Ngrok monitor task
    asyncio.create_task(monitor_ngrok_url())
    
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
