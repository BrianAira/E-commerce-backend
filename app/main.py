from fastapi import FastAPI
from sqlmodel import SQLModel
from app.infrastructure.databases.database import engine, create_db_and_tables

# Importar routers
from app.api.router.user import router as user_router
from app.api.router.cart import router as cart_router

# Crear la app de FastAPI
app = FastAPI(
    title="API eCommerce",
    description="API para gestionar usuarios y carritos",
    version="1.0.0"
)

# Incluir routers
app.include_router(user_router, tags=["Users"])
app.include_router(cart_router, tags=["Carts"])

# Crear las tablas al iniciar la app
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ Base de datos y tablas creadas")

# Ruta raíz opcional
@app.get("/")
def root():
    return {"message": "API eCommerce funcionando correctamente"}
