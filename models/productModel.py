from typing import Optional, List
from pydantic import BaseModel
from fastapi import Form, UploadFile, File
class Product(BaseModel):
    productCode: str = Form(...),
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
    categoryName: Optional[str] = Form(None),
    categoryId: str = Form(...),
    images: List[UploadFile] = File(...)

