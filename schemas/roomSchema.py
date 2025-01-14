from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class roomSchema(BaseModel):
    useremail: EmailStr
    payment:str
    check_out:datetime
    
class AddroomSchema(BaseModel):
    roomid: int
    location:str
    price:int
    status:str
    
class deleteroomSchema(BaseModel):
    roomid: int

class updateroomSchema(BaseModel):
    roomid:int
    location:Optional[str]
    price:Optional[int]
    int:Optional[str]


class updateroomSchema(BaseModel):
    roomid: int
    location: Optional[str] = None
    price: Optional[int] = None
    status: Optional[str] = None
