-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Создание дополнительных таблиц если нужно
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL
);