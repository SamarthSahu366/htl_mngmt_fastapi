from pydantic import BaseModel

class bookedSchema(BaseModel):
    roomid: int
    location: str
    price: str
    status:str
    
    class Config:
        orm_mode = True  # Enables compatibility with ORM models
