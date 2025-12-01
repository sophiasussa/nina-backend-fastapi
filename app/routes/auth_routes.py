from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate, UserLogin, UserResponse
from ..utils.password_handler import hash_password, verify_password
from ..utils.jwt_handler import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    hashed = hash_password(user.password)
    new_user = User(email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso"}

# LOGIN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = create_access_token({"sub": db_user.email})

    return {"token": token, "user": UserResponse.from_orm(db_user)}
