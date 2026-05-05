from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)