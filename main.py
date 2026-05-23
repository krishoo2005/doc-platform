from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI chal raha hai"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/search")
def search(query: str, limit: int = 10):
    return {"query": query, "limit": limit}

class Item(BaseModel):
    name: str
    price: float
    quantity: int

@app.post("/add-item")
def add_item(item: Item):
    total = item.price * item.quantity
    return {"item": item.name, "total_cost": total}

@app.get("/product/{product_id}")
def get_product(product_id: int, discount: float = 0):
    return {"product_id": product_id, "discount": discount}