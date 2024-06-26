from pydantic import BaseModel, Field


class CartItem(BaseModel):
    id: int
    quantity: int
