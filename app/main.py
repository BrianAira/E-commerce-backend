from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.core.config import settings
from app.api.router.order_router import router as order_router
from app.api.router.cart_router import router as cart_router
from app.api.router.user_router import router as user_router
from app.api.router.product_router import router as product_router
from app.api.router.category_router import router as category_router
from app.api.router.payment_router import router as payment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi Odisea")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# def on_startup():
#     init_db()

app.include_router(product_router)
app.include_router(user_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(category_router)
app.include_router(payment_router)


# app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Mi odisea api funciona"}