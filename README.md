# ⚡ TechGear — Sistema Híbrido de Catálogo y Pedidos

## 📌 Contexto

**TechGear** es una tienda virtual especializada en hardware y accesorios tecnológicos.

El proyecto utiliza una **arquitectura híbrida**:

* **FastAPI:** API REST encargada de la lógica de negocio, productos y pedidos.
* **Django:** aplicación web encargada de la interfaz y renderizado de las páginas.
* **MongoDB Atlas:** base de datos utilizada por la API para almacenar la información.

---
# 🚀 Despliegue

## FastAPI

La API puede desplegarse en **Render**.

 URL:

```text
https://taller2-7gm3.onrender.com
```
URL swagger:
https://taller2-7gm3.onrender.com/docs

Configuración:

```text
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Las variables de entorno de MongoDB deben configurarse desde el panel de Render.

## Django

El proyecto web puede desplegarse en **Vercel**.
URL:
https://taller2-mu.vercel.app/

URL para funcionalidades de administrador:
https://taller2-mu.vercel.app/administrador/productos/




## 🛠️ Tecnologías

* Python
* Django
* FastAPI
* Pydantic
* MongoDB Atlas
* HTML5
* CSS3
* Requests
* Uvicorn
* Git y GitHub

---

# 📥 Instalación

## 1. Clonar el proyecto

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git
cd proyecto
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

## 3. Instalar dependencias

Para la API:

```bash
cd techgear_api
pip install -r requirements.txt
```

Para Django:

```bash
cd ../techgear_web
pip install -r requirements.txt
```

---

# ⚙️ Configuración

Crear las variables de entorno necesarias.

### FastAPI

Configurar la conexión a MongoDB Atlas:

```env
MONGO_URI=tu_uri_de_mongodb
DATABASE_NAME=techgear
```

### Django

Configurar la URL de la API:

```env
FASTAPI_URL=http://127.0.0.1:8000
```

Para producción:

```env
FASTAPI_URL=https://taller2-7gm3.onrender.com
```

---

# ▶️ Ejecución local

## FastAPI

Desde `techgear_api`:

```bash
uvicorn main:app --reload --port 8000
```

API disponible en:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

## Django

Desde `techgear_web`:

```bash
python manage.py runserver 8001
```

Página web:

```text
http://127.0.0.1:8001
```

### Puertos utilizados

| Servicio      | Puerto |
| ------------- | -----: |
| FastAPI       | `8000` |
| Django        | `8001` |
| MongoDB Atlas | Remoto |

---


---

# ✨ Funcionalidades

### 👤 Cliente

* Visualización del catálogo.
* Consulta de productos.
* Agregar productos al carrito.
* Eliminación de productos del carrito.
* Cálculo automático de subtotales y total.
* Formulario de checkout.
* Creación de pedidos.
* Consulta de pedidos.
* Visualización del detalle de pedidos.
* Página de contacto.

### 🔧 Administrador

* Visualización de productos.
* Registro de productos.
* Edición de productos.
* Eliminación de productos.
* Gestión del inventario mediante la API.

---

# 📂 Estructura del proyecto

```text
TechGear/
│
├── techgear_api/
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── products.py
│   │   └── orders.py
│   ├── schemas/
│   ├── services/
│   └── database/
│
├── techgear_web/
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   └── catalog/
│       ├── views.py
│       ├── urls.py
│       │
│       ├── templates/
│       │   └── catalog/
│       │       ├── base.html
│       │       ├── home.html
│       │       ├── products.html
│       │       ├── cart.html
│       │       ├── checkout.html
│       │       ├── orders.html
│       │       ├── order.html
│       │       ├── contact.html
│       │       ├── admin_products.html
│       │       └── admin_product_form.html
│       │
│       └── static/
│           └── catalog/
│               └── css/
│                   ├── base.css
│                   ├── home.css
│                   ├── products.css
│                   ├── cart.css
│                   ├── checkout.css
│                   ├── orders.css
│                   └── contact.css
│
└── README.md
```

---

# 🔄 Funcionamiento

```text
Usuario
   │
   ▼
Django ──────► FastAPI ──────► MongoDB Atlas
   ▲               │
   │               │
   └───────────────┘
```

Django funciona como **cliente web**, mientras que FastAPI procesa las operaciones de productos y pedidos y se comunica con MongoDB Atlas.

---

## 👩‍💻 Ejecución rápida

```bash
# Terminal 1
cd techgear_api
venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2
cd techgear_web
venv\Scripts\activate
python manage.py runserver 8001
```

Después ingresar a:

**http://127.0.0.1:8001**
