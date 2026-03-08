import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_NAME = os.getenv("DB_NAME", "tradesync")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # API
    NEPSE_API_URL = os.getenv("NEPSE_API_URL", "https://api.nepse.com.np")
    
    # Model Settings
    LSTM_LOOKBACK = 60
    TRAIN_TEST_SPLIT = 0.8
    
settings = Settings()