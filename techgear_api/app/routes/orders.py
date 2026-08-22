from fastapi import APIRouter, HTTPException, status

from app.schemas.order import (
    OrderCreate,
    OrderResponse
)

from app.services.order_service import create_order


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


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
            detail="No se pudo crear el pedido. "
                   "Verifique los productos y el stock."
        )

    return result