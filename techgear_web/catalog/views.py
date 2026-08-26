import requests

from django.shortcuts import render, redirect


# =====================================================
# CONFIGURACIÓN DE LA API
# =====================================================

API_URL = "http://127.0.0.1:8000"


# =====================================================
# INICIO
# =====================================================

def home(request):

    return render(
        request,
        "catalog/home.html"
    )


# =====================================================
# CATÁLOGO DE PRODUCTOS
# =====================================================

def products(request):

    try:

        response = requests.get(
            f"{API_URL}/productos/",
            timeout=5
        )

        response.raise_for_status()

        products = response.json()

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
# AGREGAR PRODUCTO AL CARRITO
# =====================================================

def add_to_cart(request, product_id):

    try:

        response = requests.get(
            f"{API_URL}/productos/{product_id}",
            timeout=5
        )

        response.raise_for_status()

        product = response.json()

    except requests.RequestException:

        return redirect("product_list")


    # Obtener carrito actual
    cart = request.session.get(
        "cart",
        {}
    )


    product_id = str(product_id)


    # =================================================
    # VERIFICAR STOCK
    # =================================================

    if product.get("stock", 0) <= 0:

        return redirect("product_list")


    # =================================================
    # SI YA EXISTE EN EL CARRITO
    # =================================================

    if product_id in cart:

        cantidad_actual = cart[product_id]["cantidad"]


        # No permitir superar el stock
        if cantidad_actual < product["stock"]:

            cart[product_id]["cantidad"] += 1


    # =================================================
    # SI ES UN PRODUCTO NUEVO
    # =================================================

    else:

        cart[product_id] = {

            "nombre": product["nombre"],

            "precio": product["precio"],

            "stock": product["stock"],

            "cantidad": 1

        }


    # Guardar carrito
    request.session["cart"] = cart

    request.session.modified = True


    return redirect("cart")


# =====================================================
# VER CARRITO
# =====================================================

def cart(request):

    cart = request.session.get(
        "cart",
        {}
    )


    total = 0


    # =================================================
    # CALCULAR SUBTOTALES
    # =================================================

    for item in cart.values():

        item["subtotal"] = (
            item["precio"]
            * item["cantidad"]
        )

        total += item["subtotal"]


    return render(
        request,
        "catalog/cart.html",
        {
            "cart": cart,
            "total": total
        }
    )


# =====================================================
# ELIMINAR PRODUCTO DEL CARRITO
# =====================================================

def remove_from_cart(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )


    product_id = str(product_id)


    if product_id in cart:

        del cart[product_id]


    request.session["cart"] = cart

    request.session.modified = True


    return redirect("cart")


# =====================================================
# CHECKOUT
# =====================================================

def checkout(request):

    cart = request.session.get("cart", {})

    # ==========================================
    # SI EL CARRITO ESTÁ VACÍO
    # ==========================================

    if not cart:
        return redirect("cart")

    # ==========================================
    # CALCULAR SUBTOTALES Y TOTAL
    # ==========================================

    total = 0

    for item in cart.values():

        item["subtotal"] = (
            float(item["precio"])
            * int(item["cantidad"])
        )

        total += item["subtotal"]

    # ==========================================
    # GET
    # ==========================================

    if request.method == "GET":

        return render(
            request,
            "catalog/checkout.html",
            {
                "cart": cart,
                "total": total
            }
        )

    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        usuario = request.POST.get("usuario", "").strip()

        # ======================================
        # VALIDAR USUARIO
        # ======================================

        if not usuario:

            return render(
                request,
                "catalog/checkout.html",
                {
                    "cart": cart,
                    "total": total,
                    "error": "Debes ingresar tu nombre."
                }
            )

        # ======================================
        # CONSTRUIR LISTA DE PRODUCTOS
        # ======================================

        productos = []

        for product_id, item in cart.items():

            productos.append(
                {
                    "product_id": str(product_id),
                    "cantidad": int(item["cantidad"])
                }
            )

        # ======================================
        # DATOS QUE RECIBIRÁ FASTAPI
        # ======================================

        order_data = {
            "usuario": usuario,
            "productos": productos
        }

        # ======================================
        # MOSTRAR DATOS EN TERMINAL
        # ======================================

        print("\n========================================")
        print("ENVIANDO PEDIDO A FASTAPI")
        print("========================================")
        print(order_data)
        print("========================================\n")

        try:

            response = requests.post(
                f"{API_URL}/pedidos/",
                json=order_data,
                timeout=10
            )

            # ==================================
            # RESPUESTA FASTAPI
            # ==================================

            print("\n========================================")
            print("RESPUESTA DE FASTAPI")
            print("STATUS:", response.status_code)
            print("BODY:", response.text)
            print("========================================\n")

            # ==================================
            # PEDIDO CREADO
            # ==================================

            if response.status_code == 201:

                order = response.json()

                # Vaciar carrito
                request.session["cart"] = {}

                request.session.modified = True

                return render(
                    request,
                    "catalog/order_success.html",
                    {
                        "order": order
                    }
                )

            # ==================================
            # ERROR DE FASTAPI
            # ==================================

            try:

                error_data = response.json()

                error_message = error_data.get(
                    "detail",
                    "No se pudo crear el pedido."
                )

            except ValueError:

                error_message = (
                    "FastAPI devolvió una respuesta "
                    "que no pudo ser interpretada."
                )

            return render(
                request,
                "catalog/checkout.html",
                {
                    "cart": cart,
                    "total": total,
                    "error": error_message
                }
            )

        except requests.RequestException as e:

            print("\n========================================")
            print("ERROR DE CONEXIÓN")
            print(e)
            print("========================================\n")

            return render(
                request,
                "catalog/checkout.html",
                {
                    "cart": cart,
                    "total": total,
                    "error": (
                        "No fue posible conectarse "
                        "con FastAPI."
                    )
                }
            )

    return redirect("checkout")

    cart = request.session.get(
        "cart",
        {}
    )


    # Si no hay productos
    if not cart:

        return redirect("cart")


    total = 0


    # =================================================
    # CALCULAR SUBTOTALES
    # =================================================

    for item in cart.values():

        item["subtotal"] = (
            item["precio"]
            * item["cantidad"]
        )

        total += item["subtotal"]


    # =================================================
    # MÉTODO GET
    # =================================================

    if request.method == "GET":

        return render(
            request,
            "catalog/checkout.html",
            {
                "cart": cart,
                "total": total
            }
        )


    # =================================================
    # MÉTODO POST
    # =================================================

    if request.method == "POST":

        usuario = request.POST.get(
            "usuario"
        )


        # Validar usuario
        if not usuario:

            return render(
                request,
                "catalog/checkout.html",
                {
                    "cart": cart,
                    "total": total,
                    "error": "Debes ingresar tu nombre."
                }
            )


        # =============================================
        # CONSTRUIR PRODUCTOS PARA FASTAPI
        # =============================================

        productos = []


        for product_id, item in cart.items():

            productos.append({

                "product_id": product_id,

                "cantidad": item["cantidad"]

            })


        # =============================================
        # DATOS DEL PEDIDO
        # =============================================

        order_data = {

            "usuario": usuario,

            "productos": productos

        }


        try:

            response = requests.post(
                f"{API_URL}/pedidos/",
                json=order_data,
                timeout=10
            )


            # =========================================
            # PEDIDO CREADO
            # =========================================

            if response.status_code == 201:

                # Vaciar carrito
                request.session["cart"] = {}

                request.session.modified = True


                # Guardar temporalmente el pedido
                order = response.json()


                return render(
                    request,
                    "catalog/order_success.html",
                    {
                        "order": order
                    }
                )


            # =========================================
            # ERROR DE FASTAPI
            # =========================================

            try:

                error_data = response.json()

                error_message = error_data.get(
                    "detail",
                    "No se pudo crear el pedido."
                )

            except ValueError:

                error_message = (
                    "No se pudo crear el pedido."
                )


        except requests.RequestException:

            error_message = (
                "No fue posible conectarse "
                "con el servidor de pedidos."
            )


        # =============================================
        # MOSTRAR ERROR
        # =============================================

        return render(
            request,
            "catalog/checkout.html",
            {
                "cart": cart,
                "total": total,
                "error": error_message
            }
        )


# =====================================================
# PEDIDOS DEL USUARIO
# =====================================================

def orders(request):

    # Obtener el nombre del usuario
    usuario = request.GET.get(
        "usuario"
    )


    if not usuario:

        return render(
            request,
            "catalog/orders.html",
            {
                "orders": [],
                "error": (
                    "No se ha especificado "
                    "el usuario."
                )
            }
        )


    try:

        response = requests.get(
            f"{API_URL}/pedidos/",
            params={
                "usuario": usuario
            },
            timeout=5
        )

        response.raise_for_status()

        orders_data = response.json()


    except requests.RequestException:

        orders_data = []

        return render(
            request,
            "catalog/orders.html",
            {
                "orders": orders_data,
                "error": (
                    "No fue posible obtener "
                    "los pedidos."
                )
            }
        )


    return render(
        request,
        "catalog/orders.html",
        {
            "orders": orders_data,
            "usuario": usuario
        }
    )