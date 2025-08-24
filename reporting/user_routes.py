from fastapi import APIRouter, Depends, HTTPException, Header
from jose import jwt, JWTError
from django.contrib.auth import get_user_model
from .schemas import UserInfo
from .auth import SECRET_KEY, ALGORITHM
from .models import Farm, Farmer
from .database import SessionLocal

User = get_user_model()
router = APIRouter(prefix="/users", tags=["Users"])

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me", response_model=UserInfo)
def read_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "created_by": current_user.created_by
    } 




