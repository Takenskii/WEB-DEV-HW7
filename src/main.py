from fastapi import FastAPI, Form, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import uuid

app = FastAPI()

# Repositories (simulated with in-memory dictionaries)
class UsersRepository:
    users = {}

    def save_user(self, user):
        self.users[user['username']] = user

    def get_user(self, username):
        return self.users.get(username)

class FlowersRepository:
    flowers = {}
    
    def save_flower(self, flower):
        flower_id = str(uuid.uuid4())
        self.flowers[flower_id] = flower
        return flower_id

    def list_flowers(self):
        return list(self.flowers.values())

class PurchasesRepository:
    purchases = []

    def save_purchase(self, purchase):
        self.purchases.append(purchase)
    
    def list_purchases(self, user_id):
        return [p for p in self.purchases if p['user_id'] == user_id]

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Models
class User(BaseModel):
    username: str
    password: str
    photo_url: Optional[str] = None

class Flower(BaseModel):
    name: str
    price: float

class Purchase(BaseModel):
    user_id: str
    flower_id: str

# Sign Up (POST /signup)
@app.post("/signup")
def signup(user: User):
    UsersRepository().save_user(user.dict())
    return {"message": "User created successfully"}

# Login (POST /login)
@app.post("/login")
def login(username: str = Form(), password: str = Form()):
    user = UsersRepository().get_user(username)
    if not user or user['password'] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": "jwt_token", "token_type": "bearer"}

# Profile (GET /profile)
@app.get("/profile")
def profile(token: str = Depends(oauth2_scheme)):
    # Mock implementation, normally you'd decode token and fetch user data
    return {"username": "mock_user", "photo_url": "http://example.com/photo.jpg"}

# Flowers (GET /flowers)
@app.get("/flowers", response_model=List[Flower])
def get_flowers():
    return FlowersRepository().list_flowers()

# Add Flower (POST /flowers)
@app.post("/flowers")
def add_flower(flower: Flower):
    flower_id = FlowersRepository().save_flower(flower.dict())
    return {"flower_id": flower_id}

# Add to Cart (POST /cart/items)
@app.post("/cart/items")
def add_to_cart(flower_id: int = Form()):
    # Logic to add flower to cart, saved in cookies in this case
    return {"message": "Flower added to cart"}

# Get Cart Items (GET /cart/items)
@app.get("/cart/items")
def get_cart_items():
    # Return mock cart items
    return [
        {"id": "flower1", "name": "Rose", "price": 10.0},
        {"id": "flower2", "name": "Tulip", "price": 5.0}
    ]

# Purchase (POST /purchased)
@app.post("/purchased")
def purchase():
    # Logic to move items from cart to purchased
    return {"message": "Items purchased"}

# Get Purchases (GET /purchased)
@app.get("/purchased")
def get_purchases():
    # Return mock purchased items
    return [
        {"name": "Rose", "price": 10.0},
        {"name": "Tulip", "price": 5.0}
    ]
