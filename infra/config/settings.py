import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # App
    APP_NAME = os.getenv('APP_NAME', 'Assistente IA de Carros')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    #DEBUG = True
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'infra/data/database/carros.db')
    
    # AI Parameters
    TEMPERATURE = 0.7
    MAX_TOKENS = 500
    INTENT_TEMPERATURE = 0.1
    
    # Search Limits
    DEFAULT_SEARCH_LIMIT = 50
    MAX_CARS_DISPLAY = 10
    MAX_CARS_DETAILED = 5
    
    # Conversation
    MAX_HISTORY_MESSAGES = 6
    
    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não encontrada. Configure no arquivo .env")

settings = Settings()