from pydantic import BaseModel, Field
from typing import List


class OrderProduct(BaseModel):
    product_id: str
    cantidad: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    usuario: str = Field(..., min_length=2, max_length=100)
    productos: List[OrderProduct]


class OrderResponse(BaseModel):
    id: str
    usuario: str
    productos: List[OrderProduct]
    total: float
    estado: str