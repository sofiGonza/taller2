from bson import ObjectId

from app.database.connection import (
    orders_collection,
    products_collection
)


# =====================================================
# CONVERTIR PEDIDO A RESPUESTA
# =====================================================

def order_to_response(order):

    return {
        "id": str(order["_id"]),

        "usuario": order["usuario"],

        "productos": order["productos"],

        "total": order["total"],

        "estado": order["estado"]
    }


# =====================================================
# CREAR PEDIDO
# =====================================================

async def create_order(order_data):

    total = 0

    products = []


    # =================================================
    # RECORRER PRODUCTOS
    # =================================================

    for item in order_data.productos:


        # =============================================
        # VALIDAR OBJECT ID
        # =============================================

        if not ObjectId.is_valid(item.product_id):

            return None


        # =============================================
        # BUSCAR PRODUCTO
        # =============================================

        product = await products_collection.find_one(
            {
                "_id": ObjectId(item.product_id)
            }
        )


        if not product:

            return None


        # =============================================
        # VERIFICAR STOCK
        # =============================================

        if product["stock"] < item.cantidad:

            return None


        # =============================================
        # CALCULAR SUBTOTAL
        # =============================================

        subtotal = (
            product["precio"]
            * item.cantidad
        )


        total += subtotal


        # =============================================
        # INFORMACIÓN DEL PRODUCTO EN EL PEDIDO
        # =============================================

        products.append({

            "product_id": item.product_id,

            "nombre": product["nombre"],

            "precio": product["precio"],

            "cantidad": item.cantidad,

            "subtotal": subtotal

        })


    # =================================================
    # CREAR PEDIDO
    # =================================================

    order = {

        "usuario": order_data.usuario,

        "productos": products,

        "total": total,

        "estado": "pendiente"

    }


    # =================================================
    # GUARDAR PEDIDO
    # =================================================

    result = await orders_collection.insert_one(
        order
    )


    order["_id"] = result.inserted_id


    # =================================================
    # DESCONTAR STOCK
    # =================================================

    for item in order_data.productos:

        await products_collection.update_one(

            {
                "_id": ObjectId(item.product_id)
            },

            {
                "$inc": {
                    "stock": -item.cantidad
                }
            }

        )


    return order_to_response(order)