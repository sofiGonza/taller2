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
        views.product_list,
        name="product_list"
    ),

    path(
        "contacto/",
        views.contact,
        name="contact"
    ),

]