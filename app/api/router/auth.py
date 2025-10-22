from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.domain.models.enum import UserRol
from app.infrastructure.databases.database import get_session
from app.domain.models.user import LoginData, User, UserCreate, UserRead
from app.core.security import get_password_hash, verify_password, create_access_token
from app.domain.models.token import Token
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    password_hash=get_password_hash(user_in.password)
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        address=user_in.address,
        phone=user_in.phone,
        email=user_in.email,
        hashedPassword=password_hash,
        role=UserRol.CUSTOMER,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    access_token=create_access_token(subject=user.id)
    return {
        "user":user,
        "access_token":access_token,
        "token_type":"bearer"
    }

@router.post("/login")
def login(user_in: LoginData, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_in.email)).first()
    if not user or not verify_password(user_in.password, user.hashedPassword):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
