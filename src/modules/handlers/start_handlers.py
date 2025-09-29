from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🤖 Добро пожаловать в CRM-бот!\n\n"
        "Доступные команды:\n"
        "/clients - управление клиентами\n"
        "/orders - управление заказами\n"
        "/stats - статистика\n"
        "/help - помощь"
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📖 Помощь по CRM-боту:\n\n"
        "• /start - начать работу\n"
        "• /clients - управление клиентами\n" 
        "• /orders - управление заказами\n"
        "• /stats - статистика бизнеса\n\n"
        "Для админов:\n"
        "• /admin - панель администратора"
    )
