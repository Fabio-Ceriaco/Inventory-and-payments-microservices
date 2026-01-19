from redis_db import redis, Product, p_redis
import time

key = 'order_completed'
group = 'inventory_group'

try:
    redis.xgroup_create(key, group)  # Create a consumer group for the stream if it doesn't exist
except Exception as e:
    print("Consumer group probably exists:", e)

while True:
    try:
        # Read messages from the 'order_completed' stream as part of the consumer group
        # The params are:
        # group: the consumer group name
        # key: the stream key
        # {key: '>'}: read new messages that have not been delivered to any other consumer
        # None: block indefinitely until a message is available
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]  # Get the message payload
                try:
                    print(obj)
                    product = Product.get(obj['product_id'])  # Fetch the product from Redis
                    product.quantity -= int(obj['quantity'])  # Decrease the product quantity
                    product.save()  # Save the updated product back to Redis
                except Exception as e:
                    print(str(e))
                    p_redis.xadd('refund_order', obj, '*')  # If product not found, add to refund stream
    except Exception as e:
        print(str(e))
    time.sleep(1)
