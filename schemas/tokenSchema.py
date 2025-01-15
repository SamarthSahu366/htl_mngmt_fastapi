from pydantic import BaseModel
from typing import Optional

class TokenSchema(BaseModel):
    email:Optional[str]
    exp: Optional[int]  
    sub: Optional[str] 
    class Config:
        orm_mode = True
