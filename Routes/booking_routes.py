from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Room, Booking
from db import get_db
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from user_routes import verify_access_token 
from schemas.roomSchema import updateroomSchema

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@router.post("/bookroom")
def book_room(roomid: int, check_in: datetime, check_out: datetime, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = verify_token(token, db)
    
    room = db.query(Room).filter(Room.roomid == roomid).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.status != "available":
        raise HTTPException(status_code=400, detail="Room is already booked")

    new_booking = Booking(useremail=user.email, check_out=check_out, payment='unpaid')
    db.add(new_booking)
    db.commit()

    room.status = "booked"
    db.commit()
    
    return {"message": "Room booked successfully", "booking": new_booking}

@router.post("/cancelbooking")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = verify_token(token, db)
    
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.useremail == user.email).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not associated with the user")

    db.delete(booking)
    db.commit()
    room = db.query(Room).filter(Room.roomid == booking.room_id).first()
    if room:
        room.status = "available"
        db.commit()
    
    return {"message": "Booking canceled successfully"}



