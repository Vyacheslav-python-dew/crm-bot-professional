from aiogram import types
from aiogram.dispatcher import FSMContext
from src.core.bot import dp
from src.modules.database import get_db
from src.models.user import User
from src.models.client import Client
from src.modules.states import ClientStates

@dp.message_handler(commands=['clients'])
async def cmd_clients(message: types.Message):
    await message.answer(
        "👥 Управление клиентами:\n\n"
        "Доступные команды:\n"
        "/add_client - добавить клиента\n"
        "/list_clients - список клиентов\n"
        "/find_client - найти клиента"
    )

@dp.message_handler(commands=['add_client'])
async def cmd_add_client(message: types.Message):
    # Регистрируем пользователя если его нет
    db = next(get_db())
    
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        db.add(user)
        db.commit()
    
    await ClientStates.waiting_for_name.set()
    await message.answer("📝 Введите имя клиента:")

@dp.message_handler(state=ClientStates.waiting_for_name)
async def process_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await ClientStates.next()
    await message.answer("📞 Введите телефон клиента:")

@dp.message_handler(state=ClientStates.waiting_for_phone)
async def process_client_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    
    await ClientStates.next()
    await message.answer("📧 Введите email клиента (или '-' если нет):")

@dp.message_handler(state=ClientStates.waiting_for_email)
async def process_client_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text if message.text != '-' else None
    
    await ClientStates.next()
    await message.answer("📝 Введите заметки о клиенте (или '-' если нет):")

@dp.message_handler(state=ClientStates.waiting_for_notes)
async def process_client_notes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['notes'] = message.text if message.text != '-' else None
        
        # Сохраняем клиента в базу
        db = next(get_db())
        client = Client(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            notes=data['notes'],
            created_by=message.from_user.id
        )
        db.add(client)
        db.commit()
    
    await state.finish()
    await message.answer("✅ Клиент успешно добавлен!")

@dp.message_handler(commands=['list_clients'])
async def cmd_list_clients(message: types.Message):
    db = next(get_db())
    clients = db.query(Client).filter(Client.created_by == message.from_user.id).all()
    
    if not clients:
        await message.answer("📭 У вас пока нет клиентов")
        return
    
    response = "📋 Ваши клиенты:\n\n"
    for i, client in enumerate(clients, 1):
        response += f"{i}. {client.name}"
        if client.phone:
            response += f" - {client.phone}"
        if client.email:
            response += f" - {client.email}"
        response += "\n"
    
    await message.answer(response)

@dp.message_handler(commands=['find_client'])
async def cmd_find_client(message: types.Message):
    await message.answer("🔍 Введите имя клиента для поиска:")

@dp.message_handler(lambda message: message.text and not message.text.startswith('/'))
async def find_client_by_name(message: types.Message):
    db = next(get_db())
    clients = db.query(Client).filter(
        Client.created_by == message.from_user.id,
        Client.name.ilike(f"%{message.text}%")
    ).all()
    
    if not clients:
        await message.answer("❌ Клиенты не найдены")
        return
    
    response = "🔍 Найденные клиенты:\n\n"
    for i, client in enumerate(clients, 1):
        response += f"{i}. {client.name}"
        if client.phone:
            response += f" - {client.phone}"
        response += "\n"
    
    await message.answer(response)
