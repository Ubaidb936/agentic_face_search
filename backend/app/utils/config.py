import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SUPER_BASE_PROJECT_URL: str = os.getenv("SUPER_BASE_PROJECT_URL", "")
    SUPER_BASE_API_KEY: str = os.getenv("SUPER_BASE_API_KEY", "")
settings = Settings()