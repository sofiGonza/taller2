
import os

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


# =====================================================
# VARIABLES DE ENTORNO
# =====================================================

load_dotenv()


MONGO_URI = os.getenv(
    "MONGO_URI"
)

MONGO_DB = os.getenv(
    "MONGO_DB",
    "techgear"
)


# =====================================================
# CONEXIÓN A MONGODB
# =====================================================

client = AsyncIOMotorClient(
    MONGO_URI
)

db = client[
    MONGO_DB
]


# =====================================================
# COLECCIONES
# =====================================================

products_collection = db[
    "productos"
]

orders_collection = db[
    "pedidos"
]

usuarios_collection = db[
    "usuarios"
]

roles_collection = db[
    "roles"
]

permisos_collection = db[
    "permisos"
]
