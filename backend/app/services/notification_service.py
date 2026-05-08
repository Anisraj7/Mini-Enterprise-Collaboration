from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.services.websocket_manager import manager

def create_notification(db: Session, user_id: int, message: str):

    notification = Notification(
        user_id=user_id,
        message=message
    )

    db.add(notification)
    return notification

async def push_notification(user_id: int, message: str):
    await manager.send_message(user_id, message)
