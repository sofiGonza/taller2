from fastapi import APIRouter, HTTPException, status

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.services.product_service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create(product: ProductCreate):
    return await create_product(product)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
async def get_all():
    return await get_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_one(product_id: str):

    product = await get_product(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
async def update(
    product_id: str,
    product: ProductUpdate
):

    updated_product = await update_product(
        product_id,
        product
    )

    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return updated_product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(product_id: str):

    deleted = await delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return None