from fastapi import HTTPException


def validate_tenant_access(
    current_user,
    organization_id: int
):
    if (
        current_user.organization_id
        != organization_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Cross tenant access denied"
        )