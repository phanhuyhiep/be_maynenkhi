
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float
    quantity: int
    description: str
    categoryId: str

