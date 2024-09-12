from bson import ObjectId
from fastapi import APIRouter, Depends, Query
from models.orderModel import Order
from schema.orderSchema import list_order
from config.database import collection_order

router_order = APIRouter()

from fastapi import Query

@router_order.get("/order/")
async def get_all_order(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    order_status: str = Query(None),
    phone_number: str = Query(None)
):
    skip = (page - 1) * limit
    query = {}
    
    # Thêm điều kiện lọc vào truy vấn nếu các tham số có giá trị
    if order_status is not None:
        query["orderStatus"] = order_status
    
    if phone_number is not None:
        query["phoneNumber"] = phone_number
    
    total_items = collection_order.count_documents(query)
    orders = list_order(
        collection_order.find(query).skip(skip).limit(limit)
    )
    total_pages = (total_items + limit - 1) // limit
    
    return {
        "orders": orders,
        "current_page": page,
        "total_items": total_items,
        "total_pages": total_pages,
        "limit_pages": limit,
    }

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