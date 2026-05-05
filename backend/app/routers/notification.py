from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).all()

@router.patch("/{id}/read")
def mark_read(id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).get(id)
    notif.is_read = True
    db.commit()
    return {"msg": "updated"}