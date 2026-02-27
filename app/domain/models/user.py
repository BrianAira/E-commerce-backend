from sqlalchemy import Boolean, Column, Integer, String, Enum
import enum
from sqlalchemy.orm import relationship

from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"

class User(Base):
    __tablename__="users"
    
    id= Column(Integer,index=True, primary_key=True) 
    username= Column(String(100),index=True, nullable=True)
    email = Column(String(150),nullable=False, unique=True, index=True)
    password_hash= Column(String(255),nullable=False)
    
    role = Column(String(50), default=UserRole.CLIENT.value)
    
    is_active=Column(Boolean, default=True)
    
    directions=relationship("Directions", back_populates="user", cascade="all, delete-orphan")
    cart=relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders=relationship("Order", back_populates="user")

     
#     app/
# ├── domain/                # Nivel 0: Reglas de Oro
# │   ├── entities/          # Objetos de negocio (Ej: Product, Order)
# │   ├── exceptions/        # Errores específicos (Ej: InsufficientStock)
# │   └── ports/             # Interfaces (Contratos abstractos)
# │
# ├── application/           # Nivel 1: Coordinador (Casos de Uso)
# │   ├── use_cases/         # Lógica de flujo (Ej: ProcessCheckout.py)
# │   └── services/          # Lógica que cruza varias entidades
# │
# ├── infrastructure/        # Nivel 2: Implementación (Bajo nivel)
# │   ├── persistence/       # SQLAlchemy, Redis, etc.
# │   ├── external_apis/     # Clientes de Stripe, servicios de mail.
# │   └── framework/         # Configuración de FastAPI, logs, etc.
# │
# ├── entrypoints/           # Nivel 3: El "Disparador" (Adaptadores de entrada)
# │   ├── api/               # Tus rutas de FastAPI (Routers)
# │   └── cli/               # Scripts de consola (si los tienes)
# │
# └── main.py                # El Pegamento (Inyección de dependencias)

    
    