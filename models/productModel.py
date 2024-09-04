from typing import Optional, List
from pydantic import BaseModel
from fastapi import Form, UploadFile, File
class Product(BaseModel):
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
    categoryId: Optional[str] = Form(None),
    images: List[UploadFile] = File(...)

