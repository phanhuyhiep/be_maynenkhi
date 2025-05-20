from bson import ObjectId
from fastapi import APIRouter, Depends
from models.common import message_response, paginate_response
from schema.cartSchema import list_cart
from config.database import collection_cart
from models.cartModel import Cart

router_cart = APIRouter()

@router_cart.get("/cart/")
async def get_all_cart(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    total_items = collection_cart.count_documents({})
    total_pages = (total_items + limit - 1) // limit
    carts = list_cart(
        collection_cart.find().skip(skip).limit(limit)
    )
    return paginate_response(carts, page, total_items, total_pages, limit)


@router_cart.post("/cart/add")
async def create_cart(cart: Cart = Depends(Cart.as_form)):
    collection_cart.insert_one(dict(cart))
    return message_response("OK")
@router_cart.put("/cart/edit/{id_cart}")
async def update_cart(id_cart:str, cart: Cart = Depends(Cart.as_form)):
    collection_cart.find_one_and_update({"_id": ObjectId(id_cart)}, {"$set": dict(cart)})
    return message_response("OK")

@router_cart.delete("/cart/delete/{id_cart}")
async def delete_cart(id_cart:str):
    collection_cart.find_one_and_delete({"_id": ObjectId(id_cart)})
    return message_response("OK")