from fastapi import FastAPI

from app.routes.products import router as products_router
from app.routes.orders import router as orders_router


app = FastAPI(
    title="TechGear API",
    description="API REST para gestionar productos y pedidos de TechGear",
    version="1.0.0"
)


app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
async def root():
    return {
        "message": "TechGear API funcionando correctamente"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }