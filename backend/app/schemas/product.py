from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=5, max_length=300)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str = Field(..., min_length=2, max_length=50)
    marca: str = Field(..., min_length=2, max_length=50)


class ProductResponse(BaseModel):
    id: str
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria: str
    marca: str