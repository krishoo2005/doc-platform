from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import User
from schemas import UserCreate, UserResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users