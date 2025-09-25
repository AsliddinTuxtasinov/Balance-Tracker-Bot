from aiogram import types, Router
from aiogram.enums import ContentType
from aiogram.filters import Command  # 👈 MUHIM
from django.conf import settings

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Web App ochish",
                web_app=types.WebAppInfo(url=settings.TELEGRAM_WEBAPP_URL)
            )
        ]]
    )
    await message.answer("Quyidagi tugma orqali WebApp'ni oching 👇", reply_markup=keyboard)


@router.message(lambda msg: msg.content_type == ContentType.WEB_APP_DATA)
async def web_app_data(message: types.Message):
    await message.answer(f"Siz yubordingiz: {message.web_app_data.data}")
