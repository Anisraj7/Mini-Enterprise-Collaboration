# Mini Enterprise Collaboration Workflow

A role-based enterprise workflow application built with FastAPI and React. The project covers Phase 1 task management foundations and Phase 2 workflow/collaboration features.

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL / MySQL compatible SQLAlchemy setup
- JWT authentication with `python-jose`
- Password hashing with bcrypt via Passlib
- Python request logging

Frontend:
- React.js
- Tailwind CSS
- Axios
- React Router DOM
- Recharts
- `@dnd-kit` for Kanban drag and drop

Note: Phase 2 mentioned React Beautiful DnD. This implementation uses `@dnd-kit`, a maintained React drag/drop library already included in the project dependencies and suitable for the current React version.

## User Roles

- Admin: full access, can manage all tasks, assign users, delete tasks, view users, and provide final approvals.
- Manager: can create/manage own tasks, assign own tasks, monitor workflow, and approve manager-level approval requests.
- Employee: can view assigned tasks, update allowed task status transitions, submit approvals, and add public comments.

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
- Multi-level approval workflow with audit history
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
- Task comments modal
- Approval submission and action UI
- Approval history with actor names
- Activity log page

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

Activity:
- `GET /activity/`

## Setup

Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Update `backend/.env` with your local database URL and secret key before running migrations. The `.env` file is ignored by Git; commit `backend/.env.example` instead.

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
```

## Submission Checklist

- GitHub repository
- Swagger/Postman API testing screenshots
- Frontend workflow screenshots
- README documentation
- Working backend and frontend integration
