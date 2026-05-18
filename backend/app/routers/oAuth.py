from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.oauth_service import (
    google_login_service,
    google_callback_service,
)

router = APIRouter(
    prefix="/auth",
    tags=["OAuth"],
)


@router.get("/google")
async def google_login(
    request: Request,
):
    return await google_login_service(
        request,
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    return await google_callback_service(
        request,
        db,
    )