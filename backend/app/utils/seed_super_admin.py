from app.db.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole
from app.core.security import hash_password

db = SessionLocal()

email = "admin@super.com"

existing = db.query(User).filter(User.email == email).first()

if not existing:
    user = User(
        name="Super Admin",
        email=email,
        hashed_password=hash_password("12345678"),
        role=UserRole.SUPER_ADMIN.value,
        organization_id=None,
        is_active=True,
    )

    db.add(user)
    db.commit()

db.close()