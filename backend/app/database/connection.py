import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)

database = client.techgear

products_collection = database.products
orders_collection = database.orders


async def test_connection():
    try:
        await client.admin.command("ping")
        print("Conexión a MongoDB exitosa")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")