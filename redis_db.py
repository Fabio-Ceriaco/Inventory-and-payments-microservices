import time
from redis_om import get_redis_connection, HashModel, Field
from configs import settings
from datetime import datetime
import json



# Payment Redis connection setup

redis = get_redis_connection(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
)
#Inventory Redis connection setup
i_redis = get_redis_connection(
    host=settings.INVENTORY_REDIS_HOST,
    port=settings.INVENTORY_REDIS_PORT,
    decode_responses=True,
    username=settings.INVENTORY_REDIS_USERNAME,
    password=settings.INVENTORY_REDIS_PASSWORD,
)

class Order(HashModel):

    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Meta:
        database = redis


# Completed Order function
def order_completed(order: Order):
    time.sleep(5)  # Simulate payment processing delay
    order.status = 'completed'
    order.save()

    # we use redis streams to notify other microservices about the completed order
    # Add the completed order to the 'order_completed' stream
    # The '*' argument lets Redis assign the ID based on the current timestamp
    # The order.model_dump() converts the order object to a dictionary
    # so we can store it in the Redis stream
    # when an order is completed, we add it to the 'order_completed' stream
    # other microservices can listen to this stream to get notified about completed orders this work like an intern webhook
    # but is not exactly a webhook because we are using redis streams
    payload = {k: _to_redis_value(v) for k, v in order.model_dump().items()} # Convert order fields to Redis-storable format
    i_redis.xadd('order_completed', payload, '*')

def _to_redis_value(v):

    """Convert a value to a Redis-storable format.
    We need to convert certain data types to strings or JSON
    because Redis only supports string values.
    and datetime objects need to be converted to ISO format strings.
    Our order object contains datetime fields. that's why we need this function.
    isoformat() method converts datetime to a string in ISO 8601 format."""


    if isinstance(v, datetime):
        return v.isoformat()
    if v is None:
        return ""
    if isinstance(v, (dict, list, tuple, set)):
        return json.dumps(v, default=str)
    if isinstance(v, (str, int, float, bytes)):
        return v
    return str(v)

def format_obj(pk: str, model: HashModel) -> dict:
    order = Order.get(pk)
    return {
        "id": order.pk,
        "product_id": order.product_id,
        "price": order.price,
        "quantity": order.quantity,
        "total": order.total,
        "status": order.status
    }