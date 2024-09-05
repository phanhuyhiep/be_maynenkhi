from typing import Optional
from fastapi import Form
from pydantic import BaseModel
class Cart(BaseModel):
    quantity: float
    productId: Optional[str] = Form(None),

    @classmethod
    def as_form(
        cls,
        quantity: float = Form(...),
        productId: Optional[str] = Form(...)
    ) -> 'Cart':
        return cls(
            quantity = quantity,
            productId = productId
        )