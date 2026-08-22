import requests

from django.conf import settings
from django.shortcuts import render


def product_list(request):

    try:
        response = requests.get(
            f"{settings.FASTAPI_URL}/productos/"
        )

        response.raise_for_status()

        products = response.json()

    except requests.exceptions.RequestException as error:

        print(f"Error al consumir la API: {error}")

        products = []

    context = {
        "products": products
    }

    return render(
        request,
        "catalog/products.html",
        context
    )