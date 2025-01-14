from fastapi import FastAPI, Header, HTTPException
from Routes import user_routes
from Routes import room_routes
app=FastAPI()

app.include_router(user_routes.router)
app.include_router(room_routes.router)

@app.get('/')
def index():
    return "hey i am smrth"