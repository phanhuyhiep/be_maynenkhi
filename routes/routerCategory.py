from fastapi import APIRouter, Depends, Query
from bson import ObjectId
from models.categoryModel import Category
from config.database import collection_category
from schema.categorySchema import list_category, category_serial

router_category = APIRouter()

@router_category.get("/category/")
async def get_category(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    skip = (page - 1) * limit
    total_items = collection_category.count_documents({})
    categories = list_category(
        collection_category.find().skip(skip).limit(limit)
    )
    total_pages = (total_items + limit - 1) // limit
    return{
        "categories": categories, 
        "current_page": page,
        "total_items": total_items,
        "total_pages": total_pages,
        "limit_pages": limit,
    }

@router_category.get("/category/{id}")
async def get_one_category(id:str):
    category = category_serial(collection_category.find_one({"_id": ObjectId(id)}))
    return category

@router_category.post("/category/add")
async def create_category(category: Category = Depends(Category.as_form)):
    collection_category.insert_one(dict(category))
    return "add category successfully"
    
@router_category.put("/category/edit/{id}")
async def edit_category(id:str, category: Category):
    collection_category.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(category)})
    return "edit category successfully"
    
@router_category.delete("/category/delete/{id}")
async def delete_category(id:str):
    collection_category.find_one_and_delete({"_id": ObjectId(id)})
    return "delete category successfully"
    