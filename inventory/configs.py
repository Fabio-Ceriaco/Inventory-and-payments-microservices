import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    REDIS_USERNAME = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    PAYMENTS_REDIS_PASSWORD= os.getenv("PAYMENTS_REDIS_PASSWORD")
    PAYMENTS_REDIS_HOST= os.getenv("PAYMENTS_REDIS_HOST")
    PAYMENTS_REDIS_PORT= int(os.getenv("PAYMENTS_REDIS_PORT"))
    PAYMENTS_REDIS_USERNAME= os.getenv("PAYMENTS_REDIS_USERNAME")


settings = Config()