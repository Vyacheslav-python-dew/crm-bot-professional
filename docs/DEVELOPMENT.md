# 🛠️ Для разработчиков

Техническая документация для тех, кто хочет развивать ProfitPal CRM.

## 🏗️ Архитектура проекта

crm-bot-professional/
├── src/
│ ├── core/
│ │ └── bot.py # Основная логика бота (роутинг)
│ ├── models/ # Модели базы данных
│ │ ├── client.py # Модель клиента
│ │ ├── order.py # Модель заказа
│ │ └── user.py # Модель пользователя
│ ├── config/
│ │ └── settings.py # Настройки приложения
│ └── modules/
│ └── database.py # Работа с базой данных
├── docker-compose.yml # Конфигурация Docker
├── Dockerfile # Образ бота
├── requirements.txt # Зависимости Python
└── .env.example # Шаблон настроек
text


## 🛠️ Технологии

- **Python 3.11+** - основной язык
- **Aiogram 3.x** - фреймворк для Telegram ботов
- **SQLAlchemy 2.0** - ORM для работы с базой
- **PostgreSQL 15** - база данных
- **Docker & Docker Compose** - контейнеризация
- **Pydantic** - валидация настроек

## 🔧 Локальная разработка

### 1. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

pip install -r requirements.txt

2. Настройка базы данных
bash

# Запуск PostgreSQL в Docker
docker-compose up -d postgres

# Или установи PostgreSQL локально
sudo apt update
sudo apt install postgresql postgresql-contrib

# Создай базу данных
createdb crm_bot

3. Настройка окружения
env

DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://user:pass@localhost:5432/crm_bot

4. Запуск бота
bash

python src/main.py

🗄️ База данных
Структура таблиц:
sql

-- Клиенты
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    notes TEXT,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Заказы  
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'new',
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Миграции:
bash

# Создание миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

🧪 Тестирование
Запуск тестов:
bash

# Установи тестовые зависимости
pip install pytest pytest-asyncio

# Запусти тесты
pytest tests/ -v

Структура тестов:
text

tests/
├── conftest.py           # Фикстуры
├── test_models.py        # Тесты моделей
├── test_handlers.py      # Тесты обработчиков
└── test_database.py      # Тесты базы данных

📦 Docker разработка
Сборка образа:
bash

docker-compose build bot

# С пересборкой кэша
docker-compose build --no-cache bot

Локальный образ для тестирования:
bash

# Собери образ
docker build -t crm-bot:latest .

# Запусти контейнер
docker run -p 8000:8000 --env-file .env crm-bot:latest

🔄 CI/CD
GitHub Actions конфигурация:
yaml

name: CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          docker-compose -f docker-compose.test.yml up -d
          pytest tests/

🎯 Добавление новой функции
1. Пример: добавление команды /search
python

# src/core/bot.py
@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    """Поиск клиентов"""
    await message.answer("Введите имя для поиска:")

2. Добавление обработчика:
python

@dp.message(F.text)
async def process_search(message: types.Message):
    if message.text.startswith("Поиск:"):
        # Логика поиска
        name = message.text.replace("Поиск:", "").strip()
        # Поиск в базе данных
        # Отправка результатов

3. Обновление документации:

    Добавить команду в docs/USAGE.md

    Обновить примеры если нужно

🐛 Отладка
Включение детальных логов:
python

import logging
logging.basicConfig(level=logging.DEBUG)

Просмотр логов в Docker:
bash

docker-compose logs -f bot
docker-compose logs -f postgres

Дебаг режим:
bash

# Запуск с дебагом
docker-compose -f docker-compose.debug.yml up

# Или локально с pdb
python -m pdb src/main.py

📝 Code Style
Правила кода:

    Black для форматирования

    isort для сортировки импортов

    Flake8 для проверки стиля

    Type hints для типизации

Запуск проверок:
bash

black src/
isort src/
flake8 src/
mypy src/

🚀 Производственная сборка
Оптимизация образа:
dockerfile

# Многостадийная сборка
FROM python:3.11-slim as builder
# Установка зависимостей

FROM python:3.11-slim as production
# Копирование только необходимых файлов

Переменные окружения для продакшена:
env

DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@postgres:5432/crm_bot

🤝 Участие в разработке
Процесс контрибьютинга:

    Форкни репозиторий

    Создай ветку для функции

    Напиши код и тесты

    Проверь code style

    Создай pull request

Шаблон пул-реквеста:
markdown

## Описание изменений

- Что сделано
- Почему это нужно
- Как тестировал

## Чеклист

- [ ] Код соответствует стилю
- [ ] Добавлены тесты
- [ ] Обновлена документация
- [ ] Все тесты проходят

📞 Полезные ссылки

    Aiogram документация

    SQLAlchemy документация

    Docker документация

    Проект на GitHub

Удачи в разработке! 🚀

⬅️ Назад к документации | 💡 Планы развития
EOF
text


## 8. Добавляем шаблоны для issue:
```bash
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: 🐛 Сообщение об ошибке
about: Сообщи о проблеме чтобы мы могли ее исправить
title: '[BUG] '
labels: bug
assignees: ''

---

## Описание проблемы
Краткое описание что пошло не так

## Шаги для воспроизведения
1. Выполни команду '...'
2. Отправь данные '....'
3. Увидишь ошибку '....'

## Ожидаемое поведение
Что должно было произойти

## Фактическое поведение  
Что произошло на самом деле

## Скриншоты или логи
Если есть - приложи скриншоты или логи ошибок

## Информация о системе
- ОС: [например Ubuntu 20.04]
- Docker версия: [например 20.10.12]
- Версия бота: [если знаешь]

## Дополнительная информация
Любая другая информация о проблеме
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: 💡 Предложение новой функции
about: Предложи идею для улучшения проекта
title: '[FEATURE] '
labels: enhancement
assignees: ''

---

## Описание функции
Какая функция нужна и зачем

## Проблема которую она решает
Какую проблему пользователя решает эта функция

## Предлагаемое решение
Как это может быть реализовано

## Альтернативные решения
Какие еще есть варианты решения проблемы

## Дополнительный контекст
Любая дополнительная информация, скриншоты, примеры