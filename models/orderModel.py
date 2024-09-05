from typing import Literal
from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime

class Order(BaseModel):
    fullName: str
    phoneNumber: str
    city: str
    district: str
    commune: str
    detailAddress: str
    total: float
    productName: str
    productPrice: float
    productQuantity: float
    payment_methods: Literal[
        'Customers come to pick up at the store', #Khách hàng đến lấy tại cửa hàng
        'Free shipping only applies to Hanoi', #Miến phí vận chuyển tại khu vực Hà Nội
    ] = 'Free shipping only applies to Hanoi'  
    editBy: str
    orderStatus: Literal[
        'Pending approval', #Đang chờ duyệt
        'Order received',  #Đã duyệt
        'On delivery', #Đang vận chuyển
        'Completed', #Hoàn thành
        'Canceled' #Đã huỷ
    ] = 'Pending approval'
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    @classmethod
    def as_form(
        cls,
        fullName: str = Form(...),
        phoneNumber: str = Form(...),
        city: str = Form(...),
        district: str = Form(...),
        commune: str = Form(...),
        detailAddress: str = Form(...),
        productName: str = Form(...),
        productPrice: float = Form(...),
        productQuantity: float = Form(...),
        payment_methods: Literal[
            'Customers come to pick up at the store',
            'Free shipping only applies to Hanoi'
        ] = Form('Free shipping only applies to Hanoi'),
        editBy: str = Form(...),
        orderStatus: Literal[
            'Pending approval', #Đang chờ duyệt
            'Order received',  #Đã duyệt
            'On delivery', #Đang vận chuyển
            'Completed', #Hoàn thành
            'Canceled' #Đã huỷ
        ] = Form('Pending approval'),
    ) -> 'Order':
        total = productQuantity * productPrice
        return cls(
            fullName=fullName,
            phoneNumber=phoneNumber,
            city=city,
            district=district,
            commune=commune,
            detailAddress=detailAddress,
            total=total,
            productName=productName,
            productPrice=productPrice,
            productQuantity=productQuantity,
            editBy=editBy,
            payment_methods = payment_methods,
            orderStatus=orderStatus
        )