import asyncio
import logging
from src.core.bot import dp, bot
from src.config.settings import settings
from src.modules.database import create_tables

async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Запускаем ProfitPal CRM Бота...")
    logger.info(f"�� Бот токен: {settings.BOT_TOKEN[:10]}...")
    logger.info(f"👑 Админы: {settings.admin_ids_list}")
    
    try:
        # Создаем таблицы в БД
        await create_tables()
        
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот @{bot_info.username} успешно запущен!")
        
        # Запускаем опрос
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
