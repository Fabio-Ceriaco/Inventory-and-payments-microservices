from redis_om import get_redis_connection, HashModel, Field
from configs import settings
from datetime import datetime


# Redis connection setup

redis = get_redis_connection(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
)

# Payments Redis connection setup
p_redis = get_redis_connection(
    host=settings.PAYMENTS_REDIS_HOST,
    port=settings.PAYMENTS_REDIS_PORT,
    decode_responses=True,
    username=settings.PAYMENTS_REDIS_USERNAME,
    password=settings.PAYMENTS_REDIS_PASSWORD,
)

# Creating Models
class Product(HashModel):
    name: str
    price: float
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Meta:
        database = redis


# Helper function to format objects
def format_obj(pk: str, model: HashModel) -> dict:
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }
