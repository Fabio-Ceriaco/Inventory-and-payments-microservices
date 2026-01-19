from fastapi import FastAPI
from redis_db import Product, format_obj
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Inventory Microservice is up and running!"}

# Endpoint to get all products
@app.get("/products")
async def all_products():
    products = Product.all_pks()
    if not products:
        return {"message": "No products found"}
    return [format_obj(pk, Product) for pk in Product.all_pks()]

# Endpoint to create a new product
@app.post("/products")
async def create_product(product: Product):

    return product.save()

# Endpoint to get a product by primary key
@app.get("/products/{pk}", response_model=Product)
async def get_product(pk: str):
    product = Product.get(pk)
    if product:
        return product
    return {"message": "Product not found"}

@app.delete("/products/{pk}")
async def delete_product(pk: str):
    product = Product.get(pk)
    if product:
        product.delete(pk)
        return {"message": "Product deleted"}
    else:
        return {"message": "Product not found"}

