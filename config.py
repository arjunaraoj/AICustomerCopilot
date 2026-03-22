import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
    
    # Data files
    ATTRACTIONS_FILE = DATA_DIR / "attractions.csv"
    RESTAURANTS_FILE = DATA_DIR / "restaurants.csv"
    SHOPS_FILE = DATA_DIR / "shops.csv"
    CUSTOMERS_FILE = DATA_DIR / "customers.csv"
    TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"
    PROMOTIONS_FILE = DATA_DIR / "promotions.csv"
    
    # Agent settings
    AGENT_TIMEOUT = 30
    MAX_RETRIES = 3
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")