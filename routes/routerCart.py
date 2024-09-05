from bson import ObjectId
from fastapi import APIRouter, Depends
from schema.cartSchema import list_cart
from config.database import collection_cart
from models.cartModel import Cart

router_cart = APIRouter()

@router_cart.get("/cart/")
async def get_all_cart():
    carts = list_cart(collection_cart.find())
    return carts

@router_cart.post("/cart/add")
async def create_cart(cart: Cart = Depends(Cart.as_form)):
    collection_cart.insert_one(dict(cart))
    return "OK"
@router_cart.put("/cart/edit/{id_cart}")
async def update_cart(id_cart:str, cart: Cart = Depends(Cart.as_form)):
    collection_cart.find_one_and_update({"_id": ObjectId(id_cart)}, {"$set": dict(cart)})
    return "Edit cart successfully"

@router_cart.delete("/cart/delete/{id_cart}")
async def delete_cart(id_cart:str):
    collection_cart.find_one_and_delete({"_id": ObjectId(id_cart)})
    return "Delete cart successfully"