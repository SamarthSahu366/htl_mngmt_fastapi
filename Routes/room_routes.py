from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.roomSchema import AddroomSchema, deleteroomSchema, updateroomSchema
from models import Room ,User
from db import get_db
from dependies import admin_required

router = APIRouter()
@router.post("/addroom")
def add_room(room: AddroomSchema, db: Session = Depends(get_db), user: User = Depends(admin_required)):
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

@router.delete("/deleteroom")
def delete_room(room: deleteroomSchema, db: Session = Depends(get_db), user: User = Depends(admin_required)):
    room_to_delete = db.query(Room).filter(Room.roomid == room.roomid).first()
    if not room_to_delete:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room_to_delete)
    db.commit()
    return {"message": "Room deleted successfully"}

@router.put("/updateroom")
def update_room(room: updateroomSchema, db: Session = Depends(get_db), user: User = Depends(admin_required)):
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
