from fastapi import APIRouter
from schema.cartSchema import list_cart
from config.database import collection_cart
from models.cartModel import Cart

router_cart = APIRouter()

@router_cart.get("/cart/")
async def get_all_cart():
    carts = list_cart(collection_cart.find())
    return carts

@router_cart.post("/cart/add")
async def create_cart(cart: Cart):
    collection_cart.insert_one(dict(cart))