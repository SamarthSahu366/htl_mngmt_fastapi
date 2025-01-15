from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from db import get_db
from Routes.user_routes import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def admin_required(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, "access-token")
    print(user)
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    return user

def decode_token(token: str, db: Session):
    try:
        payload = verify_token(token,db)
        user_email = payload.get("sub")
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
