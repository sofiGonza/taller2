import requests

from django.shortcuts import render


FASTAPI_URL = "http://127.0.0.1:8000/productos/"


def home(request):

    return render(
        request,
        "catalog/home.html"
    )


def product_list(request):

    try:

        response = requests.get(
            FASTAPI_URL,
            timeout=5
        )

        response.raise_for_status()

        products = response.json()

    except requests.exceptions.RequestException as error:

        print(f"Error al consumir FastAPI: {error}")

        products = []

    return render(
        request,
        "catalog/products.html",
        {
            "products": products
        }
    )


def contact(request):

    return render(
        request,
        "catalog/contact.html"
    )