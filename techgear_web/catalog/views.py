from django.shortcuts import render, redirect
import requests
import os


FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "http://127.0.0.1:8000"
)


# =====================================================
# INICIO
# =====================================================

def home(request):

    return render(
        request,
        "catalog/home.html"
    )


# =====================================================
# CATÁLOGO
# =====================================================

def product_list(request):

    try:

        response = requests.get(
            f"{FASTAPI_URL}/productos/",
            timeout=5
        )

        if response.status_code == 200:

            products = response.json()

        else:

            products = []

    except requests.RequestException:

        products = []


    return render(
        request,
        "catalog/products.html",
        {
            "products": products
        }
    )


# =====================================================
# CONTACTO
# =====================================================

def contact(request):

    return render(
        request,
        "catalog/contact.html"
    )


# =====================================================
# CARRITO
# =====================================================

def cart(request):

    carrito = request.session.get(
        "carrito",
        []
    )

    total = 0

    for item in carrito:

        subtotal = (
            float(item["precio"])
            * int(item["cantidad"])
        )

        item["subtotal"] = subtotal

        total += subtotal

    request.session["carrito"] = carrito

    return render(
        request,
        "catalog/cart.html",
        {
            "carrito": carrito,
            "total": total
        }
    )


# =====================================================
# AGREGAR PRODUCTO AL CARRITO
# =====================================================

def add_to_cart(request, product_id):

    carrito = request.session.get(
        "carrito",
        []
    )

    try:

        response = requests.get(
            f"{FASTAPI_URL}/productos/{product_id}",
            timeout=5
        )

        if response.status_code != 200:

            return redirect(
                "product_list"
            )

        product = response.json()

    except requests.RequestException:

        return redirect(
            "product_list"
        )

    encontrado = False

    for item in carrito:

        if item["product_id"] == product_id:

            if item["cantidad"] < product["stock"]:

                item["cantidad"] += 1

            encontrado = True

            break

    if not encontrado:

        carrito.append({

            "product_id": product_id,

            "nombre": product["nombre"],

            "precio": product["precio"],

            "stock": product["stock"],

            "cantidad": 1,

            "subtotal": product["precio"]

        })

    request.session["carrito"] = carrito
    request.session.modified = True

    return redirect("cart")


# =====================================================
# ELIMINAR PRODUCTO DEL CARRITO
# =====================================================

def remove_from_cart(request, product_id):

    carrito = request.session.get(
        "carrito",
        []
    )

    carrito = [

        item

        for item in carrito

        if item["product_id"] != product_id

    ]

    request.session["carrito"] = carrito
    request.session.modified = True

    return redirect("cart")


# =====================================================
# CHECKOUT
# =====================================================

def checkout(request):

    carrito = request.session.get(
        "carrito",
        []
    )

    if not carrito:

        return redirect("cart")

    total = 0

    for item in carrito:

        item["subtotal"] = (
            float(item["precio"])
            * int(item["cantidad"])
        )

        total += item["subtotal"]

    if request.method == "POST":

        nombre = request.POST.get(
            "nombre",
            ""
        ).strip()

        apellido = request.POST.get(
            "apellido",
            ""
        ).strip()

        tipo_documento = request.POST.get(
            "tipo_documento",
            ""
        ).strip()

        numero_documento = request.POST.get(
            "numero_documento",
            ""
        ).strip()

        direccion = request.POST.get(
            "direccion",
            ""
        ).strip()

        correo = request.POST.get(
            "correo",
            ""
        ).strip()

        celular = request.POST.get(
            "celular",
            ""
        ).strip()

        usuario = (
            f"{nombre} {apellido}"
        ).strip()

        productos = []

        for item in carrito:

            productos.append({

                "product_id": item["product_id"],

                "cantidad": int(
                    item["cantidad"]
                )

            })

        cliente = {

            "nombre": nombre,

            "apellido": apellido,

            "tipo_documento": tipo_documento,

            "numero_documento": numero_documento,

            "direccion": direccion,

            "correo": correo,

            "celular": celular

        }

        pedido = {

            "usuario": usuario,

            "cliente": cliente,

            "productos": productos

        }

        try:

            response = requests.post(

                f"{FASTAPI_URL}/pedidos/",

                json=pedido,

                timeout=10

            )

            if response.status_code in [
                200,
                201
            ]:

                pedido_creado = response.json()

                pedido_creado["cliente"] = cliente

                pedido_creado[
                    "productos_detalle"
                ] = carrito

                request.session[
                    "ultimo_pedido"
                ] = pedido_creado

                request.session[
                    "carrito"
                ] = []

                request.session.modified = True

                return render(

                    request,

                    "catalog/order.html",

                    {
                        "pedido": pedido_creado
                    }

                )

            else:

                return render(

                    request,

                    "catalog/checkout.html",

                    {
                        "carrito": carrito,

                        "total": total,

                        "error": response.text

                    }

                )

        except requests.RequestException as e:

            return render(

                request,

                "catalog/checkout.html",

                {
                    "carrito": carrito,

                    "total": total,

                    "error": str(e)

                }

            )

    return render(

        request,

        "catalog/checkout.html",

        {
            "carrito": carrito,

            "total": total

        }

    )


# =====================================================
# PEDIDOS
# =====================================================

def orders(request):

    pedidos = []

    try:

        response = requests.get(
            f"{FASTAPI_URL}/pedidos/",
            timeout=10
        )

        if response.status_code == 200:

            pedidos = response.json()

        else:

            print(
                "Error obteniendo pedidos:",
                response.status_code
            )

            print(response.text)

    except requests.RequestException as e:

        print(
            "Error conectando con FastAPI:",
            e
        )

    return render(

        request,

        "catalog/orders.html",

        {
            "pedidos": pedidos
        }

    )


# =====================================================
# DETALLE DEL PEDIDO
# =====================================================

def order_detail(request, pedido_id):

    try:

        response = requests.get(
            f"{FASTAPI_URL}/pedidos/",
            timeout=10
        )

        if response.status_code != 200:

            return render(

                request,

                "catalog/orders.html",

                {
                    "pedidos": []
                }

            )

        pedidos = response.json()

        pedido = next(

            (
                p

                for p in pedidos

                if p["id"] == pedido_id

            ),

            None

        )

        if not pedido:

            return render(

                request,

                "catalog/orders.html",

                {
                    "pedidos": pedidos
                }

            )

        return render(

            request,

            "catalog/order.html",

            {
                "pedido": pedido
            }

        )

    except requests.RequestException:

        return render(

            request,

            "catalog/orders.html",

            {
                "pedidos": []
            }

        )


# =====================================================
# PANEL ADMINISTRADOR - PRODUCTOS
# =====================================================

def admin_products(request):

    products = []
    error = None

    try:

        response = requests.get(
            f"{FASTAPI_URL}/productos/",
            timeout=5
        )

        if response.status_code == 200:

            products = response.json()

        else:

            error = (
                f"FastAPI respondió con "
                f"estado {response.status_code}"
            )

    except requests.RequestException as e:

        error = (
            "No se pudo conectar con FastAPI: "
            f"{e}"
        )

    return render(

        request,

        "catalog/admin_products.html",

        {
            "products": products,
            "error": error
        }

    )


# =====================================================
# ADMIN - AGREGAR PRODUCTO
# =====================================================

def admin_product_create(request):

    error = None

    if request.method == "POST":

        product = {

            "nombre": request.POST.get(
                "nombre",
                ""
            ).strip(),

            "descripcion": request.POST.get(
                "descripcion",
                ""
            ).strip(),

            "precio": request.POST.get(
                "precio",
                "0"
            ),

            "stock": request.POST.get(
                "stock",
                "0"
            ),

            "categoria": request.POST.get(
                "categoria",
                ""
            ).strip(),

            "marca": request.POST.get(
                "marca",
                ""
            ).strip()

        }

        try:

            product["precio"] = float(
                product["precio"]
            )

            product["stock"] = int(
                product["stock"]
            )

            response = requests.post(

                f"{FASTAPI_URL}/productos/",

                json=product,

                timeout=10

            )

            if response.status_code == 201:

                return redirect(
                    "admin_products"
                )

            else:

                try:

                    api_error = response.json()

                except ValueError:

                    api_error = response.text

                error = (
                    f"No se pudo crear el producto: "
                    f"{api_error}"
                )

        except ValueError:

            error = (
                "El precio debe ser un número "
                "y el stock debe ser un número entero."
            )

        except requests.RequestException as e:

            error = (
                "No se pudo conectar con FastAPI: "
                f"{e}"
            )

    return render(

        request,

        "catalog/admin_product_form.html",

        {
            "error": error,
            "action": "create",
            "product": None
        }

    )


# =====================================================
# ADMIN - EDITAR PRODUCTO
# =====================================================

def admin_product_edit(request, product_id):

    error = None

    # -------------------------------------------------
    # OBTENER PRODUCTO
    # -------------------------------------------------

    try:

        response = requests.get(

            f"{FASTAPI_URL}/productos/{product_id}",

            timeout=5

        )

        if response.status_code != 200:

            return redirect(
                "admin_products"
            )

        product = response.json()

    except requests.RequestException:

        return redirect(
            "admin_products"
        )

    # -------------------------------------------------
    # ACTUALIZAR
    # -------------------------------------------------

    if request.method == "POST":

        product_data = {

            "nombre": request.POST.get(
                "nombre",
                ""
            ).strip(),

            "descripcion": request.POST.get(
                "descripcion",
                ""
            ).strip(),

            "precio": request.POST.get(
                "precio",
                "0"
            ),

            "stock": request.POST.get(
                "stock",
                "0"
            ),

            "categoria": request.POST.get(
                "categoria",
                ""
            ).strip(),

            "marca": request.POST.get(
                "marca",
                ""
            ).strip()

        }

        try:

            product_data["precio"] = float(
                product_data["precio"]
            )

            product_data["stock"] = int(
                product_data["stock"]
            )

            response = requests.put(

                f"{FASTAPI_URL}/productos/{product_id}",

                json=product_data,

                timeout=10

            )

            if response.status_code == 200:

                return redirect(
                    "admin_products"
                )

            else:

                try:

                    api_error = response.json()

                except ValueError:

                    api_error = response.text

                error = (
                    f"No se pudo actualizar: "
                    f"{api_error}"
                )

        except ValueError:

            error = (
                "El precio debe ser un número "
                "y el stock debe ser un número entero."
            )

        except requests.RequestException as e:

            error = (
                "No se pudo conectar con FastAPI: "
                f"{e}"
            )

    return render(

        request,

        "catalog/admin_product_form.html",

        {
            "error": error,
            "action": "edit",
            "product": product
        }

    )


# =====================================================
# ADMIN - ELIMINAR PRODUCTO
# =====================================================

def admin_product_delete(request, product_id):

    if request.method != "POST":

        return redirect(
            "admin_products"
        )

    try:

        response = requests.delete(

            f"{FASTAPI_URL}/productos/{product_id}",

            timeout=10

        )

        if response.status_code == 204:

            return redirect(
                "admin_products"
            )

    except requests.RequestException as e:

        print(
            "Error eliminando producto:",
            e
        )

    return redirect(
        "admin_products"
    )