from pydantic import BaseModel,EmailStr,date
from datetime import date

class roomSchema(BaseModel):
    useremail: EmailStr
    payment:str
    check_out:date
    
    class Config:
        orm_mode = True  # Enables compatibility with ORM models
