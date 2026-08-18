# Estructura del proyecto
```taller2/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── product_service.py
│   │       └── order_service.py
│   │
│   ├── .env
│   ├── .gitignore
│   └── requirements.txt
│
├── frontend/
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
│       │       ├── home.html
│       │       ├── products.html
│       │       └── orders.html
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