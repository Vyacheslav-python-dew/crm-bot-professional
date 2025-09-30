# 🔧 Решение проблем

Здесь собраны решения частых проблем и ответы на вопросы.

## 🚨 Бот не запускается

### Проверь статус сервисов:
```bash
docker-compose ps

Должно быть:
text

Name                          Command              State    Ports
crm-bot-professional-bot-1      python src/main.py          Up
crm-bot-professional-postgres-1 docker-entrypoint.sh postgres Up

Если сервисы не запущены:
bash

# Перезапусти все сервисы
docker-compose restart

# Или полностью пересобери
docker-compose down
docker-compose up -d

🤖 Бот не отвечает в Telegram
1. Проверь токен бота

Убедись что в файле .env правильный токен:
env

BOT_TOKEN=правильный_токен_здесь

Как проверить токен:

    Найди @BotFather в Telegram

    Отправь /mybots

    Выбери своего бота

    Нажми API Token

2. Проверь что бот запущен
bash

docker-compose logs bot

В логах должно быть:
text

✅ Бот @ИмяТвоегоБота успешно запущен!

3. Проверь что написал боту

    Найди бота по username в поиске Telegram

    Напиши ему первым сообщением /start

    Бот должен ответить приветствием

🗄️ Проблемы с базой данных
База не подключилась:
bash

# Проверь логи базы данных
docker-compose logs postgres

# Перезапусти базу данных
docker-compose restart postgres

Пропали данные:
bash

# Сделай бэкап
docker-compose exec postgres pg_dump -U crm_user crm_bot > backup.sql

# Восстанови базу
docker-compose down
docker-compose up -d

📝 Ошибки при добавлении данных
"Ошибка при добавлении клиента"

Проблема: Неправильный формат данных

Правильный формат:
text

Имя Фамилия | Телефон | Email | Заметки

Пример правильного ввода:
text

Анна Петрова | +79998887766 | anna@mail.ru | Заказывала дизайн визиток

"Клиент не найден" при создании заказа

Проблема: Неправильный ID клиента

Решение:

    Посмотри список клиентов: /clients

    Найди правильный ID клиента

    Используй этот ID при создании заказа

🔧 Технические проблемы
Докер не запускается
bash

# Проверь что Docker установлен
docker --version
docker-compose --version

# Если нет - установи Docker

Не хватает места на диске
bash

# Почисти ненужные образы
docker system prune

# Удали все неиспользуемые данные
docker system prune -a

Обновление версии
bash

# Останови старую версию
docker-compose down

# Скачай обновления
git pull

# Запусти новую версию
docker-compose up -d

📞 Если ничего не помогло
Собери информацию для разработчика:
bash

# Версия Docker
docker --version
docker-compose --version

# Логи бота
docker-compose logs bot

# Логи базы данных  
docker-compose logs postgres

# Статус сервисов
docker-compose ps

Напиши разработчику:

    Опиши проблему подробно

    Приложи логи ошибок

    Укажи свою ОС и версию Docker

🛡️ Профилактика проблем
Регулярное обслуживание:
bash

# Раз в месяц делай бэкап
docker-compose exec postgres pg_dump -U crm_user crm_bot > backup_$(date +%Y%m%d).sql

# Следи за свободным местом
df -h

# Обновляй образы
docker-compose pull

Мониторинг работы:
bash

# Раз в неделю проверяй логи
docker-compose logs bot --tail=20

# Следи за потреблением ресурсов
docker stats

Помни: Большинство проблем решается простым перезапуском!
bash

docker-compose restart