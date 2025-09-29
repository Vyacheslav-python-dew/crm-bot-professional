from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Обязательные поля
    BOT_TOKEN: str
    ADMIN_IDS: str  # Храним как строку
    
    # Опциональные поля с значениями по умолчанию
    DATABASE_URL: str = "postgresql://crm_user:!1245Bot@postgres:5432/crm_bot"
    DEBUG: bool = True

    @property
    def admin_ids_list(self) -> List[int]:
        """Парсим ADMIN_IDS в список чисел"""
        try:
            return [int(x.strip()) for x in self.ADMIN_IDS.split(",")]
        except:
            return [7832164413]  # fallback

    @property
    def BOT_USERNAME(self):
        return "ProfitPal_CRM_Bot"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
