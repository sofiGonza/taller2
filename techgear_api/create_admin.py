import asyncio
import bcrypt
from datetime import datetime

from app.database.connection import db


# ============================================================
# DATOS DEL ADMINISTRADOR
# ============================================================

ADMIN_DATA = {
    "nombre": "Administrador",
    "apellido": "TechGear",
    "tipoDocumento": "CC",
    "numeroDocumento": "1000000000",
    "direccion": "TechGear",
    "telefono": "3000000000",
    "correo": "admin@techgear.com",
    "password": "Admin123*",
}


# ============================================================
# CREAR ROL ADMINISTRADOR
# ============================================================

async def obtener_o_crear_rol():

    roles_collection = db["roles"]

    rol = await roles_collection.find_one({
        "nombre": "administrador"
    })

    if rol:
        print("✅ El rol administrador ya existe.")
        return rol

    print("⚠️ El rol administrador no existe.")
    print("Creando rol administrador...")

    nuevo_rol = {
        "nombre": "administrador",
        "descripcion": "Administrador del sistema",
        "permisos": [
            "crear_producto",
            "leer_producto",
            "actualizar_producto",
            "eliminar_producto",
            "crear_usuario",
            "leer_usuario",
            "actualizar_usuario",
            "eliminar_usuario",
            "gestionar_pedidos"
        ],
        "fecha_creacion": datetime.utcnow()
    }

    resultado = await roles_collection.insert_one(nuevo_rol)

    nuevo_rol["_id"] = resultado.inserted_id

    print("✅ Rol administrador creado.")

    return nuevo_rol


# ============================================================
# CREAR ADMINISTRADOR
# ============================================================

async def crear_administrador():

    usuarios_collection = db["usuarios"]

    # --------------------------------------------------------
    # Obtener / crear rol
    # --------------------------------------------------------

    rol = await obtener_o_crear_rol()

    # --------------------------------------------------------
    # Verificar si ya existe el administrador
    # --------------------------------------------------------

    admin_existente = await usuarios_collection.find_one({
        "correo": ADMIN_DATA["correo"]
    })

    if admin_existente:

        print()
        print("⚠️ Ya existe un usuario con este correo:")
        print(f"   {ADMIN_DATA['correo']}")
        print()

        return

    # --------------------------------------------------------
    # Validar contraseña
    # --------------------------------------------------------

    password = ADMIN_DATA["password"]

    if len(password.encode("utf-8")) > 72:

        print("❌ La contraseña supera los 72 bytes permitidos por bcrypt.")
        return

    # --------------------------------------------------------
    # Encriptar contraseña
    # --------------------------------------------------------

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # --------------------------------------------------------
    # Crear administrador
    # --------------------------------------------------------

    nuevo_admin = {
        "nombre": ADMIN_DATA["nombre"],
        "apellido": ADMIN_DATA["apellido"],
        "tipoDocumento": ADMIN_DATA["tipoDocumento"],
        "numeroDocumento": ADMIN_DATA["numeroDocumento"],
        "direccion": ADMIN_DATA["direccion"],
        "telefono": ADMIN_DATA["telefono"],
        "correo": ADMIN_DATA["correo"],
        "password": password_hash,
        "rol": rol["_id"],
        "activo": True,
        "fecha_creacion": datetime.utcnow()
    }

    resultado = await usuarios_collection.insert_one(nuevo_admin)

    print()
    print("==========================================")
    print("     ✅ ADMINISTRADOR CREADO")
    print("==========================================")
    print()
    print(f"ID:       {resultado.inserted_id}")
    print(f"Nombre:   {ADMIN_DATA['nombre']} {ADMIN_DATA['apellido']}")
    print(f"Correo:   {ADMIN_DATA['correo']}")
    print(f"Password: {ADMIN_DATA['password']}")
    print("Rol:      administrador")
    print()
    print("==========================================")
    print("Puedes utilizar estos datos para iniciar")
    print("sesión en el panel administrativo.")
    print("==========================================")
    print()


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    asyncio.run(crear_administrador())