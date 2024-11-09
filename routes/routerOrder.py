from typing import Optional
from bson import ObjectId
from bson.json_util import dumps
from fastapi import APIRouter, Depends, HTTPException, Query
from models.orderModel import Order, StatusOrder
from schema.orderSchema import list_order, order_serial
from config.database import collection_order
import random
import string

router_order = APIRouter()


def generate_random_code(length: int = 7) -> str:
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


from pymongo import DESCENDING

router_order = APIRouter()


@router_order.get("/order/")
async def get_all_order(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    order_status: Optional[str] = Query(None),
    searchTerm: Optional[str] = Query(None),
):
    skip = (page - 1) * limit
    query = {}
    if order_status:
        query["orderStatus"] = order_status
    if searchTerm:
        query["$or"] = [{"phoneNumber": searchTerm}, {"orderCode": searchTerm}]
    total_items = collection_order.count_documents(query)
    orders = list_order(
        collection_order.find(query).skip(skip).limit(limit).sort([("_id", DESCENDING)])
    )
    total_pages = (total_items + limit - 1) // limit
    return {
        "orders": orders,
        "current_page": page,
        "total_items": total_items,
        "total_pages": total_pages,
        "limit": limit,
    }


@router_order.get("/order/{order_id}")
async def get_order_by_id(order_id: str):
    try:
        order = collection_order.find_one({"_id": ObjectId(order_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid order ID format.")
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order_serial(order)


@router_order.post("/order/add")
async def create_order(order: Order = Depends(Order.as_form)):
    order.orderCode = generate_random_code()
    collection_order.insert_one(dict(order))
    return "Message: OK"


@router_order.put("/order/edit/{id_order}")
async def edit_order(id_order: str, order: Order = Depends(Order.as_form)):
    order_data = dict(order)
    if "orderCode" in order_data:
        del order_data["orderCode"]
    collection_order.find_one_and_update(
        {"_id": ObjectId(id_order)}, {"$set": order_data}
    )
    return "Edit order OK"


@router_order.patch("/order/edit-status/{id_order}")
async def edit_order_status(
    id_order: str, status_data: StatusOrder = Depends(StatusOrder.as_form)
):
    update_result = collection_order.find_one_and_update(
        {"_id": ObjectId(id_order)}, {"$set": {"orderStatus": status_data.orderStatus}}
    )

    if update_result:
        return "Edit status order OK"
    else:
        raise HTTPException(status_code=404, detail="Order not found")


@router_order.delete("/order/delete/{id_order}")
async def delete_order(id_order: str):
    collection_order.find_one_and_delete({"_id": ObjectId(id_order)})
    return "Delete order OK"
