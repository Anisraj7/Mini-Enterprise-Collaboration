from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.database import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"))

    plan = Column(String, default="basic")

    credits = Column(Integer, default=100)

    status = Column(String, default="active")

    start_date = Column(DateTime, default=datetime.utcnow)

    end_date = Column(DateTime)