# Mini Enterprise Collaboration Workflow

A role-based enterprise workflow application built with FastAPI and React. The project now covers task management, workflow collaboration, and Phase 3 enterprise features: document handling, audit logs, notifications, real-time updates, and dashboard intelligence.

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL / MySQL compatible SQLAlchemy setup
- File upload/download handling
- JWT authentication with `python-jose`
- Password hashing with bcrypt via Passlib
- Python request logging
- WebSockets for live notifications

Frontend:
- React.js
- Tailwind CSS
- Axios
- React Router DOM
- Recharts
- `@dnd-kit` for Kanban drag and drop
- React Hot Toast
- Lucide React icons

Note: Phase 2 mentioned React Beautiful DnD. This implementation uses `@dnd-kit`, a maintained React drag/drop library already included in the project dependencies and suitable for the current React version.

## User Roles

- Admin: full access, can manage tasks, assign users, delete tasks, view users, view audit logs, access documents, and provide final approvals.
- Manager: can create/manage own tasks, assign own tasks, monitor workflow, access team task documents, and approve manager-level requests.
- Employee: can view assigned tasks, update allowed task status transitions, upload/download authorized documents, submit approvals, and add public comments.

## Backend Features

- JWT login and protected endpoints
- Role-based access control dependencies
- User registration and current-user endpoint
- Task CRUD with role-based visibility
- Task assignment workflow
- Kanban board API
- Validated task transitions: `todo -> in_progress -> review -> done`
- Task status history tracking
- Task comments with public/internal notes
- Activity logging for task, comment, and approval actions
- Immutable-style audit logs for enterprise actions
- Multi-level approval workflow with audit history
- Document upload, versioning, task document listing, and secure download
- User-scoped notifications with read/unread state
- WebSocket endpoint for live notification delivery
- AI-style dashboard summary for pending, high-priority, and delayed tasks
- Dashboard summary and task distribution APIs
- HTTP request logging with method, path, status, and duration

## Frontend Features

- Login and registration screens
- Protected routing
- Dashboard with task summary and charts
- Task list with role-based actions
- Create and edit task screens
- User listing for admins
- Kanban board with drag/drop
- Task comments, documents, and assignment actions in the Kanban modal
- Approval submission and action UI
- Approval history with actor names
- Activity log page
- Dashboard notification panel and activity feed

## API Overview

Authentication:
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Users:
- `GET /users/`
- `GET /users/assignable`
- `GET /users/{user_id}`

Tasks:
- `POST /tasks/`
- `GET /tasks/`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `PATCH /tasks/{task_id}/assign`
- `GET /tasks/kanban`
- `PATCH /tasks/{task_id}/status`

Comments:
- `POST /tasks/{task_id}/comments`
- `GET /tasks/{task_id}/comments`

Approvals:
- `POST /approvals/`
- `GET /approvals/`
- `PATCH /approvals/{approval_id}/action`
- `GET /approvals/{approval_id}/history`

Dashboard:
- `GET /dashboard/summary`
- `GET /dashboard/task-distribution`
- `GET /dashboard/approvals`
- `GET /dashboard/ai-summary`

Activity:
- `GET /activity/`

Documents:
- `POST /documents/upload?task_id={task_id}`
- `GET /documents/task/{task_id}`
- `GET /documents/{document_id}`

Audit Logs:
- `GET /audit-logs/`

Notifications:
- `GET /notifications/`
- `PATCH /notifications/{notification_id}/read`

Realtime:
- `WS /ws/{user_id}`

## Setup

Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m alembic upgrade head
uvicorn app.main:app --reload
```

Update `backend/.env` with your local database URL and secret key before running migrations. The `.env` file is ignored by Git; commit `backend/.env.example` instead.

Example PostgreSQL URL:

```env
DATABASE_URL=postgresql://postgres:password@localhost/enterprisecollab
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Default URLs:
- Backend API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Frontend: `http://127.0.0.1:5173`

## Verification

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

Backend:

```bash
cd backend
python -m compileall app
python -m alembic current
```

## Submission Checklist

- GitHub repository
- Swagger/Postman API testing screenshots
- Frontend workflow screenshots
- README documentation
- Working backend and frontend integration
