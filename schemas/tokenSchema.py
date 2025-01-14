from pydantic import BaseModel
from typing import Optional

class TokenSchema(BaseModel):
    exp: Optional[int]  
    sub: Optional[str] 
    class Config:
        orm_mode = True
