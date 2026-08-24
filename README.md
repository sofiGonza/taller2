## cómo iniciar cada servidor.
# link desplegado de FastAPI
https://taller2-7gm3.onrender.com


# Documentacion en Swagger
https://taller2-7gm3.onrender.com/docs


# FastAPI

cd techgear_api

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
Django


## otra terminal:

cd techgear_web

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver 8001



FastAPI:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

Django:
http://127.0.0.1:8001

# Estructura del proyecto
```taller2/
│
├── techgear_api/
│   ├── app/
│   │   ├── main.py
│   │   ├── database/
│   │   │   └── connection.py
│   │   ├── schemas/
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   ├── routes/
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   └── services/
│   │       ├── product_service.py
│   │       └── order_service.py
│   │
│   ├── .env
│   ├── .gitignore
│   └── requirements.txt
│
├── techgear_web/
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── catalog/
│       ├── migrations/
│       ├── templates/
│       │   └── catalog/
│       │       ├── base.html
│       │       └── products.html
│       │
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
│
├── README.md
└── .gitignore```