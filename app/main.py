from fastapi import FastAPI
from sqlmodel import SQLModel
from app.infrastructure.databases.database import engine, create_db_and_tables

# Importar routers
from app.api.router.user import router as user_router
from app.api.router.cart import router as cart_router
from app.api.router.product import router as product_router
from app.api.router.order import router as order_router
from app.api.router.order_item import router as order_item_router
from app.api.router.cart_item import router as cart_item_router

from app.api.router.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
# Crear la app de FastAPI
app = FastAPI(
    title="API eCommerce",
    description="API para gestionar usuarios y carritos",
    version="1.0.0"
)

origins=[
    "http://localhost:5173",  # tu frontend
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(user_router, tags=["Users"])
app.include_router(cart_router, tags=["Carts"])
app.include_router(product_router, tags=["Products"])
app.include_router(order_router, tags=["Orders"])
app.include_router(order_item_router, tags=["Order_items"])
app.include_router(cart_item_router,tags=["CartItem"])

app.include_router(auth_router, tags=["Auth"])
# Crear las tablas al iniciar la app
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ Base de datos y tablas creadas")

# Ruta raíz opcional
@app.get("/")
def root():
    return {"message": "API eCommerce funcionando correctamente"}
