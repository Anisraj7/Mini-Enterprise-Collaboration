from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.core.dependencies import get_current_user

from app.db.database import get_db

from app.schemas.comments import (
    CommentCreate,
    CommentOut,
)

from app.services.comment_service import (
    create_comment_service,
    get_comments_service,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Comments"],
)


@router.post(
    "/{task_id}/comments",
    response_model=CommentOut,
)
def add_comment(
    task_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_comment_service(
        task_id,
        payload,
        user,
        db,
    )


@router.get(
    "/{task_id}/comments",
    response_model=Page[CommentOut],
)
def list_comments(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_comments_service(
        task_id,
        user,
        db,
    )