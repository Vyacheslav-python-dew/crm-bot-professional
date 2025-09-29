from aiogram import types
from src.core.bot import dp
from src.modules.database import get_db
from src.models.client import Client

@dp.message_handler(commands=['stats'])
async def cmd_stats(message: types.Message):
    db = next(get_db())
    
    # Считаем статистику
    total_clients = db.query(Client).filter(Client.created_by == message.from_user.id).count()
    
    await message.answer(
        f"📊 Ваша статистика:\n\n"
        f"• Всего клиентов: {total_clients}\n"
        f"• Активных заказов: 0\n"
        f"• Завершенных сделок: 0\n\n"
        f"Продолжайте в том же духе! 💪"
    )
