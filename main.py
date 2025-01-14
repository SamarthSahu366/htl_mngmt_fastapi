from fastapi import FastAPI, Header, HTTPException
from Routes import user_routes
from models import User
app=FastAPI()

app.include_router(user_routes.router)
# app.include_router(user_routes.rou)

@app.get('/')
def index():
    return "hey i am smrth"