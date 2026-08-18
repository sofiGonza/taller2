from bson import ObjectId

from app.database.connection import products_collection


def product_to_response(product):
    return {
        "id": str(product["_id"]),
        "nombre": product["nombre"],
        "descripcion": product["descripcion"],
        "precio": product["precio"],
        "stock": product["stock"],
        "categoria": product["categoria"],
        "marca": product["marca"],
    }


async def create_product(product_data):
    product = product_data.model_dump()

    result = await products_collection.insert_one(product)

    product["_id"] = result.inserted_id

    return product_to_response(product)


async def get_products():
    products = []

    async for product in products_collection.find():
        products.append(product_to_response(product))

    return products


async def get_product(product_id):
    if not ObjectId.is_valid(product_id):
        return None

    product = await products_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    if not product:
        return None

    return product_to_response(product)


async def update_product(product_id, product_data):
    if not ObjectId.is_valid(product_id):
        return None

    update_data = {
        key: value
        for key, value in product_data.model_dump().items()
        if value is not None
    }

    if not update_data:
        return await get_product(product_id)

    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None

    return await get_product(product_id)


async def delete_product(product_id):
    if not ObjectId.is_valid(product_id):
        return False

    result = await products_collection.delete_one(
        {"_id": ObjectId(product_id)}
    )

    return result.deleted_count > 0