from django.urls import path
from . import views


urlpatterns = [

    # =================================================
    # INICIO
    # =================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =================================================
    # CATÁLOGO
    # =================================================

    path(
        "catalogo/",
        views.product_list,
        name="product_list"
    ),


    # =================================================
    # CONTACTO
    # =================================================

    path(
        "contacto/",
        views.contact,
        name="contact"
    ),


    # =================================================
    # CARRITO
    # =================================================

    path(
        "carrito/",
        views.cart,
        name="cart"
    ),

    path(
        "carrito/agregar/<str:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "carrito/eliminar/<str:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),


    # =================================================
    # CHECKOUT
    # =================================================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =================================================
    # PEDIDOS
    # =================================================

    path(
        "pedidos/",
        views.orders,
        name="orders"
    ),

    path(
        "pedidos/<str:pedido_id>/",
        views.order_detail,
        name="order_detail"
    ),


    # =================================================
    # PANEL ADMINISTRADOR
    # =================================================

    path(
        "administrador/productos/",
        views.admin_products,
        name="admin_products"
    ),

    path(
        "administrador/productos/agregar/",
        views.admin_product_create,
        name="admin_product_create"
    ),

    path(
        "administrador/productos/editar/<str:product_id>/",
        views.admin_product_edit,
        name="admin_product_edit"
    ),

    path(
        "administrador/productos/eliminar/<str:product_id>/",
        views.admin_product_delete,
        name="admin_product_delete"
    ),

]