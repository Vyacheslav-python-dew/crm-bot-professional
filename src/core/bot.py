from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.config.settings import settings
from src.models.client import Client
from src.models.order import Order
from src.modules.database import AsyncSessionLocal

# Создаем бота
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# ========== КЛИЕНТЫ ==========

@dp.message(Command("clients"))
async def cmd_clients(message: types.Message):
    """Показать список клиентов"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Client).where(Client.created_by == message.from_user.id)
        )
        clients = result.scalars().all()
        
        if clients:
            clients_text = "📋 <b>Ваши клиенты:</b>\n\n"
            for i, client in enumerate(clients, 1):
                clients_text += f"{i}. <b>{client.name}</b>\n"
                if client.phone:
                    clients_text += f"   📞 {client.phone}\n"
                if client.email:
                    clients_text += f"   📧 {client.email}\n"
                if client.notes:
                    clients_text += f"   📝 {client.notes}\n"
                clients_text += f"   🆔 ID: {client.id}\n\n"
            
            await message.answer(clients_text, parse_mode=ParseMode.HTML)
        else:
            await message.answer(
                "📋 <b>У вас пока нет клиентов</b>\n\n"
                "Добавьте первого клиента командой:\n"
                "<code>/add_client</code>",
                parse_mode=ParseMode.HTML
            )

@dp.message(Command("add_client"))
async def cmd_add_client(message: types.Message):
    """Добавить нового клиента"""
    await message.answer(
        "👤 <b>Добавление клиента</b>\n\n"
        "Отправьте данные клиента в формате:\n"
        "<code>Имя Клиента | Телефон | Email | Заметки</code>\n\n"
        "<b>Пример:</b>\n"
        "<code>Иван Иванов | +79991234567 | ivan@mail.ru | Постоянный клиент</code>\n\n"
        "�� <i>Телефон, email и заметки - необязательные</i>\n"
        "💡 <i>Можно использовать только имя и телефон</i>",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text.regexp(r'^[^|]+\|'))
async def process_add_client(message: types.Message):
    """Обработка добавления клиента"""
    try:
        parts = [part.strip() for part in message.text.split('|')]
        name = parts[0]
        
        # Умное определение полей
        phone = None
        email = None
        notes = None
        
        if len(parts) > 1:
            # Проверяем, похож ли второй параметр на телефон
            second_part = parts[1]
            if any(char.isdigit() for char in second_part) and ('@' not in second_part):
                phone = second_part
                if len(parts) > 2:
                    # Третий параметр - проверяем на email
                    third_part = parts[2]
                    if '@' in third_part and '.' in third_part:
                        email = third_part
                        if len(parts) > 3:
                            notes = parts[3]
                    else:
                        notes = third_part
            else:
                # Второй параметр не похож на телефон - возможно это email или заметки
                if '@' in second_part and '.' in second_part:
                    email = second_part
                    if len(parts) > 2:
                        notes = parts[2]
                else:
                    notes = second_part
        
        async with AsyncSessionLocal() as session:
            client = Client(
                name=name,
                phone=phone,
                email=email,
                notes=notes,
                created_by=message.from_user.id
            )
            session.add(client)
            await session.commit()
            await session.refresh(client)
            
            response_text = f"✅ <b>Клиент добавлен!</b>\n\n👤 <b>Имя:</b> {client.name}\n"
            if client.phone:
                response_text += f"📞 <b>Телефон:</b> {client.phone}\n"
            if client.email:
                response_text += f"📧 <b>Email:</b> {client.email}\n"
            if client.notes:
                response_text += f"📝 <b>Заметки:</b> {client.notes}\n"
            response_text += f"🆔 <b>ID клиента:</b> {client.id}"
            
            await message.answer(response_text, parse_mode=ParseMode.HTML)
            
    except Exception as e:
        await message.answer(
            "❌ <b>Ошибка при добавлении клиента</b>\n\n"
            "Проверьте формат данных и попробуйте снова.\n"
            f"Ошибка: {str(e)}",
            parse_mode=ParseMode.HTML
        )

# ========== ЗАКАЗЫ ==========

@dp.message(Command("orders"))
async def cmd_orders(message: types.Message):
    """Показать список заказов"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order).where(Order.created_by == message.from_user.id)
        )
        orders = result.scalars().all()
        
        if orders:
            orders_text = "📦 <b>Ваши заказы:</b>\n\n"
            for i, order in enumerate(orders, 1):
                status_emoji = {
                    "new": "🆕",
                    "in_progress": "🔄", 
                    "completed": "✅",
                    "cancelled": "❌"
                }.get(order.status, "📦")
                
                orders_text += f"{i}. {status_emoji} <b>{order.title}</b>\n"
                orders_text += f"   💰 Сумма: {order.amount} руб.\n"
                orders_text += f"   📊 Статус: {order.status}\n"
                orders_text += f"   🆔 ID: {order.id}\n\n"
            
            await message.answer(orders_text, parse_mode=ParseMode.HTML)
        else:
            await message.answer(
                "📦 <b>У вас пока нет заказов</b>\n\n"
                "Создайте первый заказ командой:\n"
                "<code>/add_order</code>",
                parse_mode=ParseMode.HTML
            )

@dp.message(Command("add_order"))
async def cmd_add_order(message: types.Message):
    """Добавить новый заказ"""
    await message.answer(
        "📦 <b>Создание заказа</b>\n\n"
        "Отправьте данные заказа в формате:\n"
        "<code>Название заказа | Сумма | ID клиента | Описание</code>\n\n"
        "<b>Пример:</b>\n"
        "<code>Разработка сайта | 50000 | 1 | Создание корпоративного сайта</code>\n\n"
        "💡 <i>Описание - необязательное</i>\n"
        "💡 <i>ID клиента можно посмотреть командой /clients</i>",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text.regexp(r'^[^|]+\|\s*\d+\.?\d*\|\s*\d+'))
async def process_add_order(message: types.Message):
    """Обработка создания заказа"""
    try:
        parts = [part.strip() for part in message.text.split('|')]
        title = parts[0]
        amount = float(parts[1])
        client_id = int(parts[2])
        description = parts[3] if len(parts) > 3 else None
        
        async with AsyncSessionLocal() as session:
            # Проверяем существование клиента
            client_result = await session.execute(
                select(Client).where(
                    Client.id == client_id,
                    Client.created_by == message.from_user.id
                )
            )
            client = client_result.scalar_one_or_none()
            
            if not client:
                await message.answer(
                    "❌ <b>Клиент не найден!</b>\n\n"
                    "Проверьте ID клиента и попробуйте снова.\n"
                    "Список ваших клиентов: /clients",
                    parse_mode=ParseMode.HTML
                )
                return
            
            order = Order(
                title=title,
                amount=amount,
                client_id=client_id,
                description=description,
                created_by=message.from_user.id
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            
            await message.answer(
                f"✅ <b>Заказ создан!</b>\n\n"
                f"📦 <b>Название:</b> {order.title}\n"
                f"💰 <b>Сумма:</b> {order.amount} руб.\n"
                f"👤 <b>Клиент:</b> {client.name}\n"
                f"📊 <b>Статус:</b> {order.status}\n"
                f"📝 <b>Описание:</b> {order.description or 'нет'}\n"
                f"🆔 <b>ID заказа:</b> {order.id}",
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        await message.answer(
            "❌ <b>Ошибка при создании заказа</b>\n\n"
            "Проверьте формат данных и попробуйте снова.\n"
            f"Ошибка: {str(e)}",
            parse_mode=ParseMode.HTML
        )

# ========== СТАТИСТИКА ==========

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """Показать статистику"""
    async with AsyncSessionLocal() as session:
        # Статистика клиентов
        clients_count = await session.execute(
            select(func.count(Client.id)).where(Client.created_by == message.from_user.id)
        )
        clients_total = clients_count.scalar()
        
        # Статистика заказов
        orders_count = await session.execute(
            select(func.count(Order.id)).where(Order.created_by == message.from_user.id)
        )
        orders_total = orders_count.scalar()
        
        # Сумма всех заказов
        total_amount = await session.execute(
            select(func.sum(Order.amount)).where(Order.created_by == message.from_user.id)
        )
        total_revenue = total_amount.scalar() or 0
        
        await message.answer(
            f"📊 <b>Ваша статистика</b>\n\n"
            f"👥 <b>Клиентов:</b> {clients_total}\n"
            f"📦 <b>Заказов:</b> {orders_total}\n"
            f"💰 <b>Общая сумма:</b> {total_revenue} руб.\n\n"
            f"🚀 <b>ProfitPal CRM</b>",
            parse_mode=ParseMode.HTML
        )

# ========== СУЩЕСТВУЮЩИЕ КОМАНДЫ ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user
    
    # Используем правильную проверку админа
    is_admin = user.id in settings.admin_ids_list
    
    await message.answer(
        f"👋 <b>Добро пожаловать в ProfitPal CRM Бот!</b>\n\n"
        f"🆔 Ваш ID: <code>{user.id}</code>\n"
        f"👤 Имя: {user.first_name}\n"
        f"🎯 Статус: {'✅ Администратор' if is_admin else '👤 Пользователь'}\n\n"
        f"📋 <b>Команды CRM:</b>\n"
        f"/clients - мои клиенты\n"
        f"/add_client - добавить клиента\n"
        f"/orders - мои заказы\n"
        f"/add_order - создать заказ\n"
        f"/stats - статистика\n"
        f"/profile - профиль\n"
        f"/admin - админка\n\n"
        f"🚀 <b>ProfitPal CRM</b> - профессиональное управление клиентами",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>ProfitPal CRM Бот</b>\n\n"
        "📊 <b>Функции:</b>\n"
        "• Управление клиентами\n"
        "• Создание заказов\n"
        "• Статистика продаж\n\n"
        "👑 <b>Для админов:</b>\n"
        "• Просмотр статистики\n"
        "• Управление пользователями\n\n"
        "🔧 Используйте команды из меню!",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = message.from_user
    is_admin = user.id in settings.admin_ids_list
    
    await message.answer(
        f"📊 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Имя: {user.first_name}\n"
        f"📛 Фамилия: {user.last_name or 'не указана'}\n"
        f"🔗 Username: @{user.username or 'не указан'}\n"
        f"🎯 Статус: {'✅ Администратор' if is_admin else '👤 Пользователь'}\n\n"
        f"💼 <b>ProfitPal CRM</b>",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    user = message.from_user
    
    if user.id not in settings.admin_ids_list:
        await message.answer("⛔ <b>У вас нет прав администратора</b>", parse_mode=ParseMode.HTML)
        return
        
    await message.answer(
        "👨💼 <b>Панель администратора</b>\n\n"
        "✅ <b>Доступ разрешен</b>\n"
        f"🆔 Ваш ID: <code>{user.id}</code>\n\n"
        "📈 <b>Система готова к работе!</b>\n\n"
        "�� Следующие шаги:\n"
        "• Добавление клиентов\n"
        "• Создание заказов\n"
        "• Настройка уведомлений",
        parse_mode=ParseMode.HTML
    )

# Обработчик любого текста (не команд)
@dp.message(F.text)
async def echo_message(message: types.Message):
    await message.answer(
        "🤖 <b>ProfitPal CRM Бот</b>\n\n"
        "Используйте команды:\n"
        "/start - начать работу\n"
        "/help - помощь\n"
        "/profile - ваш профиль\n"
        "/admin - админка",
        parse_mode=ParseMode.HTML
    )
