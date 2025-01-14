from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True