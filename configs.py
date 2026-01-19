import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    REDIS_USERNAME = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    INVENTORY_REDIS_HOST = os.getenv("INVENTORY_REDIS_HOST")
    INVENTORY_REDIS_USERNAME = os.getenv("INVENTORY_REDIS_USERNAME")
    INVENTORY_REDIS_PASSWORD = os.getenv("INVENTORY_REDIS_PASSWORD")
    INVENTORY_REDIS_PORT = int(os.getenv("INVENTORY_REDIS_PORT"))


settings = Config()