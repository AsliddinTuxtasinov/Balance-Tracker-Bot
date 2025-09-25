import os
import sys

import aiohttp
import django
import asyncio

# project_root -> backend papkasi (apps va core shu yerda joylashgan)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings
from apps.telegram_bot.config import bot, dp
from apps.telegram_bot.handlers import start


# Routerlarni ro‘yxatga olish
all_routers = [
    start.router,
]


async def on_startup():
    """
    Ngrok orqali public URL olib, uni Django settings va webhookga yozish
    """
    async with aiohttp.ClientSession() as session:
        async with session.get("http://ngrok:4040/api/tunnels") as resp:
            data = await resp.json()
            public_url = data["tunnels"][0]["public_url"]  # https://xxxxx.ngrok-free.app

    # Django settings ichiga dinamik yozib qo‘yamiz
    settings.TELEGRAM_WEBAPP_URL = public_url

    # Webhook URL -> shu public ngrok domain
    webhook_url = f"{public_url}/webhook"
    print(f"🌍 Ngrok public URL: {public_url}")
    print(f"🔗 Webhook URL: {webhook_url}")

    # Eski webhookni tozalab, yangisini qo‘yish
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(webhook_url)


# Async main
async def main():
    # Routerlarni ulash
    for router in all_routers:
        dp.include_router(router)

    # Startup event (ngrok URL olish + webhook set qilish)
    await on_startup()

    print("🚀 Bot ishga tushdi ...")
    # Webhook rejimida ishlaydi (polling emas)
    # Agar polling kerak bo‘lsa, dp.start_polling(bot) ni ishlatasiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
