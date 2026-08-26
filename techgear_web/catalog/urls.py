from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "catalogo/",
        views.products,
        name="product_list"
    ),

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

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "pedidos/",
        views.orders,
        name="orders"
    ),

    path(
        "contacto/",
        views.contact,
        name="contact"
    ),
]