from typing import Optional
from pydantic import BaseModel, Field
# from fastapi import Email
# from bson import ObjectId
class Category(BaseModel):
    name: str
    
class Product(BaseModel):
    name: str
    price: float
    quantity: int
    description: str
    categoryId: str


class Auth(BaseModel):
    name: Optional[str] = None
    email: str
    password: str
    role: str = Field(default="USER")