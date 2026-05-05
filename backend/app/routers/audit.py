from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.audit import AuditLog

router = APIRouter(prefix="/audit-logs", tags=["Audit"])

@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).all()