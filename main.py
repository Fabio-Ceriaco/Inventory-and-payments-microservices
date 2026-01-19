from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
import requests
from redis_db import redis, Order, order_completed, format_obj

# FastAPI app initialization
app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Payments Microservice is up and running!"}

@app.get("/orders/{pk}")
async def get_order(pk: str):
    return Order.get(pk)

@app.get("/orders")
async def get_orders():
    orders = Order.all_pks()
    if not orders:
        return {"message": "No orders found"}
    return [format_obj(pk, Order) for pk in Order.all_pks()]

# Endpoint to create a new order
@app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks):
    # Get the JSON body from the request to do this in postman or frontend
    # Fetch product details from the Inventory microservice
    # Make a GET request to the Inventory microservice to get product details
    # in postman we make a post request to /orders with a body in json containing the product id and quantity
    # in json format: { "id": "product_id", "quantity": 2 } because we have body = await request.json()
    # and we access body['id'] and body['quantity']
    body = await request.json()

    # this is the request that we will make to the inventory microservice to get the product details
    req = requests.get("http://localhost:8000/products/%s" % body['id'])
    product = req.json()
    # Create a new order
    if product['quantity'] < body['quantity']:
        return {"message": "Not enough product items in stock"}
    elif product['quantity'] == 0:
        return {"message": "Product out of stock"}
    else:
        order = Order(
            product_id=body['id'], # the product id from the body

            price=product['price'], # the price from the product details
            fee=product['price'] * 0.2, # 20% fee
            total=(product['price'] * 1.2) * body['quantity'], # total price including fee
            quantity=body['quantity'], # quantity from the body
        )
        # Save the order to Redis
        order.save()

        # Simulate payment processing and mark the order as completed
        # In fastapi we can use background tasks to run a function in the background
        # Use background tasks to avoid blocking the main thread
        # Add the order_completed function to background tasks
        # and pass the order as an argument
        background_tasks.add_task(order_completed, order)

        return order



@app.delete("/order/{pk}")
async def delete_order(pk: str):
    order = Order.get(pk)
    if order:
        order.delete(pk)
        return {"message": "Order deleted"}
    else:
        return {"message": "Order not found"}