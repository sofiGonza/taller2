from pydantic import BaseModel, Field, EmailStr
from typing import List


# =====================================================
# PRODUCTO QUE SE ENVÍA AL CREAR EL PEDIDO
# =====================================================

class OrderProduct(BaseModel):

    product_id: str

    cantidad: int = Field(
        ...,
        gt=0
    )


# =====================================================
# DATOS DEL CLIENTE
# =====================================================

class CustomerData(BaseModel):

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    apellido: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    tipo_documento: str = Field(
        ...,
        min_length=2,
        max_length=20
    )

    numero_documento: str = Field(
        ...,
        min_length=5,
        max_length=20
    )

    direccion: str = Field(
        ...,
        min_length=5,
        max_length=150
    )

    correo: EmailStr

    celular: str = Field(
        ...,
        min_length=7,
        max_length=20
    )


# =====================================================
# CREACIÓN DEL PEDIDO
# =====================================================

class OrderCreate(BaseModel):

    usuario: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    cliente: CustomerData

    productos: List[OrderProduct]


# =====================================================
# PRODUCTO EN LA RESPUESTA
# =====================================================

class OrderProductResponse(BaseModel):

    product_id: str

    nombre: str

    precio: float

    cantidad: int

    subtotal: float


# =====================================================
# RESPUESTA DEL PEDIDO
# =====================================================

class OrderResponse(BaseModel):

    id: str

    usuario: str

    cliente: CustomerData

    productos: List[OrderProductResponse]

    total: float

    estado: str