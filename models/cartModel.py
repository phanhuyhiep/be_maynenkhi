from pydantic import BaseModel
class Cart(BaseModel):
    nameProduct: str
    imgProduct: str
    priceProduct: str
    quantity: str