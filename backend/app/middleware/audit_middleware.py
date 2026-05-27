import json
import time

from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from fastapi import Request

from app.db.database import (
    SessionLocal,
)

from app.models.audit_log import (
    AuditLog,
)


class AuditMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        start_time = time.time()

        response = await call_next(
            request
        )

        process_time = (
            time.time() - start_time
        )

        # =====================================
        # TRACK ONLY WRITE OPERATIONS
        # =====================================
        if request.method in [
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]:

            db = SessionLocal()

            try:

                user = getattr(
                    request.state,
                    "user",
                    None,
                )

                user_id = (
                    getattr(user, "id", None)
                    if user
                    else None
                )

                organization_id = (
                    getattr(
                        user,
                        "organization_id",
                        None,
                    )
                    if user
                    else None
                )

                ip_address = (
                    request.client.host
                    if request.client
                    else None
                )

                user_agent = (
                    request.headers.get(
                        "user-agent"
                    )
                )

                path = request.url.path

                module_name = (
                    path.split("/")[1]
                    if len(
                        path.split("/")
                    ) > 1
                    else "unknown"
                )

                audit_log = AuditLog(
                    user_id=user_id,
                    organization_id=organization_id,
                    module_name=module_name,
                    action_type=request.method,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    new_data=json.dumps(
                        {
                            "path": path,
                            "method": request.method,
                            "status_code": response.status_code,
                            "process_time": process_time,
                        }
                    ),
                )

                db.add(audit_log)

                db.commit()

            except Exception as e:

                print(
                    "Audit middleware error:",
                    e,
                )

            finally:

                db.close()

        return response