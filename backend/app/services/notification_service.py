from sqlalchemy.orm import Session
from app.models.notification import Notification

def create_notification(db: Session, user_id, message):
    notif = Notification(user_id=user_id, message=message)
    db.add(notif)
    db.commit()