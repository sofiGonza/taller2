from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.order import (
    OrderCreate,
    OrderResponse
)

from app.services.order_service import (
    create_order,
    get_orders
)


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# =====================================================
# CREAR PEDIDO
# =====================================================

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
async def create(order: OrderCreate):

    result = await create_order(order)

    if not result:

        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo crear el pedido. "
                "Verifique los productos y el stock."
            )
        )

    return result


# =====================================================
# OBTENER PEDIDOS
# =====================================================

@router.get(
    "/",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_orders():

    orders = await get_orders()

    return orders