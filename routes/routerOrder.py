from bson import ObjectId
from fastapi import APIRouter, Depends
from models.orderModel import Order
from schema.orderSchema import list_order
from config.database import collection_order

router_order = APIRouter()

@router_order.get("/order/")
async def get_all_order():
    orders = list_order(collection_order.find())
    return orders

@router_order.post("/order/add")
async def create_order(order:Order = Depends(Order.as_form)):
    collection_order.insert_one(dict(order))
    return "Message: OK"

@router_order.put("/order/edit/{id_order}")
async def edit_order(id_order: str, order: Order = Depends(Order.as_form)):
    collection_order.find_one_and_update({"_id": ObjectId(id_order)}, {"$set": dict(order)})
    return "Edit order OK"

@router_order.delete("/order/delete/{id_order}")
async def delete_order(id_order: str):
    collection_order.find_one_and_delete({"_id": ObjectId(id_order)})
    return "Delete order OK"