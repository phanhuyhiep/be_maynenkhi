import cloudinary.uploader
import cloudinary
from fastapi import APIRouter, File,UploadFile, HTTPException,Form, Path
from bson import ObjectId
from typing import Optional, List
from models.productModel import Product
from config.database import collection_product
from schema.productSchema import list_product, product_serial
import os
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

load_dotenv()

CLOUD_NAME = os.getenv('CLOUD_NAME')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

router_product = APIRouter()

cloudinary.config(
    cloud_name= CLOUD_NAME,
    api_key = API_KEY,
    api_secret= API_SECRET
)

@router_product.post("/product/add")
async def create_product(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
    categoryId: Optional[str] = Form(None),
    images: List[UploadFile] = File(...)
):
    try:
        image_urls = []
        # Xử lý từng hình ảnh
        for image in images:
            # Đọc nội dung hình ảnh
            image_content = await image.read()
            # Tải lên Cloudinary và lấy URL
            upload_result = cloudinary.uploader.upload(image_content)
            # Lấy URL hình ảnh từ kết quả trả về
            image_url = upload_result.get('secure_url')
            if not image_url:
                raise HTTPException(status_code=500, detail="Image upload failed, secure_url not found")
            image_urls.append(image_url)
        product = {
            "name": name,
            "images": image_urls,  # Cập nhật với danh sách URL hình ảnh
            "price": price,
            "quantity": quantity,
            "description": description,
            "categoryId": categoryId
        }
        result = collection_product.insert_one(product)
        created_product = collection_product.find_one({"_id": result.inserted_id})
        return product_serial(created_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload images: {str(e)}")
@router_product.get("/product/")
async def get_all_product():
    products = list_product(collection_product.find())
    return products
    
@router_product.get("/product/{id}")
async def get_one_product(id: str):
    product = collection_product.find_one({"_id": ObjectId(id)})
    return product_serial(product)

@router_product.put("/product/edit/{product_id}")
async def edit_product(
    product_id: str = Path(..., description="ID của sản phẩm cần chỉnh sửa"),
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    quantity: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    categoryId: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None)
):
    try:
        product_id_obj = ObjectId(product_id)

        # Tìm sản phẩm cũ
        existing_product = collection_product.find_one({"_id": product_id_obj})
        if not existing_product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        # Xử lý hình ảnh nếu có
        image_urls = []
        if images:
            for image in images:
                image_content = await image.read()
                upload_result = cloudinary.uploader.upload(image_content)
                image_url = upload_result.get('secure_url')
                if not image_url:
                    raise HTTPException(status_code=500, detail="Image upload failed, secure_url not found")
                image_urls.append(image_url)

        # Cập nhật thông tin sản phẩm
        updated_product = {
            "name": name if name is not None else existing_product.get("name"),
            "price": price if price is not None else existing_product.get("price"),
            "quantity": quantity if quantity is not None else existing_product.get("quantity"),
            "description": description if description is not None else existing_product.get("description"),
            "categoryId": categoryId if categoryId is not None else existing_product.get("categoryId"),
            "images": image_urls if image_urls else existing_product.get("images"),
        }
        # Cập nhật sản phẩm trong cơ sở dữ liệu
        collection_product.update_one({"_id": product_id_obj}, {"$set": updated_product})
        # Lấy sản phẩm đã cập nhật
        updated_product_data = collection_product.find_one({"_id": product_id_obj})
        if updated_product_data is None:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found after update")

        # Chuyển đổi ObjectId thành chuỗi
        updated_product_data["_id"] = str(updated_product_data["_id"])

        # Trả về sản phẩm đã cập nhật
        return jsonable_encoder(updated_product_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")
@router_product.delete("/product/delete/{id}")
async def delete_product(id:str):
    collection_product.find_one_and_delete({"_id": ObjectId(id)})
    return "delete successfully"