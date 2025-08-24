from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from jose import jwt
from .schemas import Token
from .deps import *
from pydantic import BaseModel

SECRET_KEY = "django-insecure-2(sv9z9l##69r1@95918=+=(2c6@rxkww_k1dcc#jtad*l60cn"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

User = get_user_model()
router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=Token)
def login(login_data: LoginRequest):
    user = User.objects.filter(username=login_data.username).first()
    if not user or not check_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=1))
    return {"access": access_token, "refresh": refresh_token}












