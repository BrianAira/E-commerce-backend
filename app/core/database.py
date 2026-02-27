
from sqlmodel import create_engine
from .config import settings
from sqlalchemy.orm import sessionmaker, declarative_base

engine=create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=60*30, 
    pool_pre_ping=True,
    # echo=True
    )

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()


# Dependencia para obtener la sesión en cada request
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_session():
#     with Session(engine) as session:
#         yield session
        
# def init_db():
#     #Crear las tablas si aun no existen.
#     SQLModel.metadata.create_all(engine)