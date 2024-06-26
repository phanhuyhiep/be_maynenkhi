from fastapi import APIRouter
from bson import ObjectId
from models.productModel import Product
from config.database import collection_product
from schema.productSchema import list_product, product_serial

router_product = APIRouter()

@router_product.post("/product/add")
async def create_product(product: Product):
    collection_product.insert_one(dict(product))
    
@router_product.get("/product/")
async def get_all_product():
    products = list_product(collection_product.find())
    return products
    
@router_product.get("/product/{id}")
async def get_one_product(id: str):
    product = collection_product.find_one({"_id": ObjectId(id)})
    return product_serial(product)

@router_product.put("/product/edit/{id}")
async def update_product(id: str, product: Product):
    collection_product.find_one_and_update({"_id" : ObjectId(id)}, {"$set": dict(product)})

@router_product.delete("/product/delete/{id}")
async def delete_product(id:str):
    collection_product.find_one_and_delete({"_id": ObjectId(id)})