from bson import ObjectId

from app.database.connection import (
    orders_collection,
    products_collection
)


def order_to_response(order):
    return {
        "id": str(order["_id"]),
        "usuario": order["usuario"],
        "productos": order["productos"],
        "total": order["total"],
        "estado": order["estado"]
    }


async def create_order(order_data):

    total = 0
    products = []

    for item in order_data.productos:

        if not ObjectId.is_valid(item.product_id):
            return None

        product = await products_collection.find_one(
            {"_id": ObjectId(item.product_id)}
        )

        if not product:
            return None

        if product["stock"] < item.cantidad:
            return None

        subtotal = product["precio"] * item.cantidad

        total += subtotal

        products.append({
            "product_id": item.product_id,
            "cantidad": item.cantidad
        })

    order = {
        "usuario": order_data.usuario,
        "productos": products,
        "total": total,
        "estado": "pendiente"
    }

    result = await orders_collection.insert_one(order)

    order["_id"] = result.inserted_id

    return order_to_response(order)