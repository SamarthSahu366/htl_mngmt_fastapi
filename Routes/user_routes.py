from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from passlib.context  import CryptContext
from models import User as UserModel
from schemas.userSchema import UserSchema
from schemas.userLoginSchema import UserLoginSchema
import bcrypt
from jose import jwt
from models import User
from datetime import datetime,timedelta,timezone
from  fastapi.security import OAuth2PasswordBearer
from schemas.protected_schema import TokenSchema
from schemas.tokenSchema import TokenSchema
from schemas.userSchema import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

SECRET_KEY='nogutsnoglory'
REFRESH_SECRET_KEY='NOPAINNNOGAIN'
refresh_token_expires=7

reuseable_oath=OAuth2PasswordBearer(tokenUrl='/login',scheme_name="JWT")

def hash_password(password:str)->str:
    return pwd_context.hash(password)    

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

@router.post("/users/protected_route")
def protected_route(token: str = Depends(reuseable_oath), db: Session = Depends(get_db)):
    token_email=verify_token(token,"access-token")
    user = db.query(User).filter(User.email == token_email).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    else:
        return {"message": "User found", "user": user}

@router.get('/users/signup')
def signin_get():
    return 'this is a sign up page'

@router.post('/users/signup')
def signin_post(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password=hash_password(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_token(token: str, token_type: str):
    try:
        if token_type == "access-token":
            payload = verify_access_token(token)
        elif token_type == "refresh-token":
            payload = verify_refresh_token(token)
        else:
            raise HTTPException(status_code=400, detail="Invalid token type")
        return payload
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

        
def verify_access_token(token: TokenSchema):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(status_code=403, detail="Token has expired")
        return email
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def verify_refresh_token(token: TokenSchema):
    try:
        # print("Decoding refresh token...")
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=['HS256'])
        # print(f"Decoded payload: {payload}")
        email = payload.get("email")
        print(email)
        if not email:
            raise HTTPException(status_code=403, detail="Invalid token payload: email not found")
        exp = payload.get("exp")
        if not exp or datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=403, detail="Token has expired")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.JWTError as e:
        print(f"JWTError: {e}")
        raise HTTPException(status_code=403, detail="Could not validate credentials")


def generate_access_token(email: str):
    payload = {
        "email": email, 
        "exp": datetime.utcnow()+timedelta(hours=12),
        "sub": "anything"
    }
    token = jwt.encode(payload,SECRET_KEY, algorithm='HS256')
    return token

def create_access_token(email: str):
    payload = {
        "email": email, 
        "exp": datetime.utcnow()+timedelta(hours=12),
        "sub": "anything"
    }
    token = jwt.encode(payload,REFRESH_SECRET_KEY, algorithm='HS256')
    return token

@router.post('/users/login')
def login_post(user: UserLoginSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    else:
        user_given_pass = user.password
        db_user_pass = existing_user.password
        if bcrypt.checkpw(user_given_pass.encode('utf-8'), db_user_pass.encode('utf-8')):
            access_token = generate_access_token(user.email)
            refresh_token = create_access_token(user.email)
            return {"access_token": access_token,"refresh_token":refresh_token}
        else:
            raise HTTPException(status_code=504, detail="Incorrect password")


    
