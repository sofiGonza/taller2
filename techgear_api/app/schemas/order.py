from pydantic import BaseModel, Field
from typing import List


# =====================================================
# PRODUCTO QUE LLEGA AL CREAR EL PEDIDO
# =====================================================

class OrderProduct(BaseModel):

    product_id: str

    cantidad: int = Field(
        ...,
        gt=0
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

    productos: List[OrderProduct]


# =====================================================
# PRODUCTO QUE DEVUELVE EL PEDIDO
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

    productos: List[OrderProductResponse]

    total: float

    estado: str