from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Room, Booking, User
from db import get_db
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from user_routes import verify_access_token 
from schemas.roomSchema import updateroomSchema

router = APIRouter()

# OAuth2 Password Bearer (assuming you're using JWT tokens)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function to verify token (you can adjust to your own implementation)
def verify_token(token: str, db: Session):
    # Decode the token and get user data (e.g., user email)
    try:
        payload = verify_access_token(token)  # Assuming you have this function
        user_email = payload.get("sub")
        
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Route to book a room
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

# Route to cancel a booking
@router.post("/cancelbooking")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = verify_token(token, db)
    
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.useremail == user.email).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not associated with the user")

    db.delete(booking)
    db.commit()

    # Find and update the room status
    room = db.query(Room).filter(Room.roomid == booking.room_id).first()
    if room:
        room.status = "available"
        db.commit()
    
    return {"message": "Booking canceled successfully"}

# Admin required function to check if user is admin (example)
def admin_required(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    
    return user

# Route to add a room (Admin required)
@router.post("/addroom")
def add_room(room: AddroomSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = admin_required(token, db)  # Verify if user is an admin
    
    new_room = Room(
        roomid=room.roomid,
        location=room.location,
        price=room.price,
        status=room.status
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {"message": "Room added successfully", "room": new_room}

# Route to delete a room (Admin required)
@router.delete("/deleteroom")
def delete_room(room: deleteroomSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = admin_required(token, db)  # Verify if user is an admin
    
    room_to_delete = db.query(Room).filter(Room.roomid == room.roomid).first()
    if not room_to_delete:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db.delete(room_to_delete)
    db.commit()
    return {"message": "Room deleted successfully"}

# Route to update a room (Admin required)
@router.put("/updateroom")
def update_room(room: updateroomSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = admin_required(token, db)  # Verify if user is an admin
    
    room_to_update = db.query(Room).filter(Room.roomid == room.roomid).first()
    if not room_to_update:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.location:
        room_to_update.location = room.location
    if room.price:
        room_to_update.price = room.price
    if room.status:
        room_to_update.status = room.status
    
    db.commit()
    db.refresh(room_to_update)
    return {"message": "Room updated successfully", "room": room_to_update}
