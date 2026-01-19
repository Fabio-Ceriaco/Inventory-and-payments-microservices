from redis_db import redis, Order
import time

key = 'refund_order'
group = 'payment_group'

try:
    redis.xgroup_create(key, group) # Create a consumer group for the stream if it doesn't exist
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
            print(results)
            for result in results:
                obj = result[1][0][1] # Get the message payload
                order = Order.get(obj['pk']) # Fetch the product from Redis
                order.status = 'refunded' # Change order status to refund
                order.save() # Save the updated order back to Redis
    except Exception as e:
        print(str(e))
    time.sleep(1)