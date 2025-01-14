from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True  # Enables compatibility with ORM models
