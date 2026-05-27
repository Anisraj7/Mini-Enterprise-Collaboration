# Mini Enterprise Collaboration Workflow

A full-stack enterprise collaboration app built with FastAPI and React. It supports role-based task management, workflow approvals, comments, documents, activity/audit logs, notifications, real-time updates, OAuth login, payment plans, and dashboard reporting.

## Tech Stack

Backend:
- FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic v2
- PostgreSQL via `psycopg2-binary`
- JWT authentication with `python-jose`
- Password hashing with Passlib bcrypt
- Redis-backed optional caching
- SlowAPI rate limiting
- Authlib Google OAuth
- Razorpay and Stripe payment integrations
- FastAPI Pagination
- WebSockets for live notifications

Frontend:
- React 19 and Vite
- Tailwind CSS
- Axios
- React Router DOM
- Recharts
- `@dnd-kit` for Kanban drag and drop
- React Hot Toast
- Lucide React and React Icons

## Code Structure

```text
Mini Enterprise Collaboration/
├── README.md
├── .gitignore
├── uploads/
├── backend/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── .env.example
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── database migration files
│   └── app/
│       ├── main.py
│       ├── core/
│       │   ├── config.py
│       │   ├── security.py
│       │   ├── dependencies.py
│       │   ├── permissions.py
│       │   ├── rate_limit.py
│       │   ├── cache.py
│       │   └── celery_app.py
│       ├── db/
│       │   └── database.py
│       ├── models/
│       │   └── SQLAlchemy database models
│       ├── schemas/
│       │   └── Pydantic request/response schemas
│       ├── repository/
│       │   └── Database access layer
│       ├── services/
│       │   └── Business logic layer
│       ├── routers/
│       │   └── FastAPI route handlers
│       ├── middleware/
│       │   └── audit_middleware.py
│       ├── tasks/
│       │   └── Celery/background tasks
│       └── utils/
│           └── credits.py
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    ├── public/
    │   ├── favicon.svg
    │   └── icons.svg
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── api/
        │   ├── axios.js
        │   ├── pagination.js
        │   └── websocket.js
        ├── components/
        │   ├── Navbar.jsx
        │   ├── NotificationPanel.jsx
        │   └── ProtectedRoute.jsx
        └── pages/
            ├── Login.jsx
            ├── Register.jsx
            ├── Dashboard.jsx
            ├── Users.jsx
            ├── CreateTask.jsx
            ├── AssignTask.jsx
            ├── EditTask.jsx
            ├── KanbanBoard.jsx
            ├── Approval.jsx
            ├── Activity.jsx
            ├── Billing.jsx
            ├── PaymentSuccess.jsx
            └── OAuthCallback.jsx
```

## User Roles

- Admin: full access to users, tasks, assignments, audit logs, documents, approvals, and enterprise actions.
- Manager: create/manage own tasks, assign tasks, monitor workflows, access team task documents, and handle manager approvals.
- Employee: view assigned tasks, follow allowed task transitions, upload/download authorized documents, submit approvals, and comment.

## Features

- JWT login, refresh tokens, password reset, and protected routes
- Google OAuth login
- Role-based API authorization
- Task CRUD, assignment, smart assignment, and status workflow
- Kanban board APIs and drag/drop frontend
- Task comments with public/internal notes
- Activity logging and audit log viewing
- Multi-level approvals with action history
- Document upload, versioning, task document listing, and secure download
- User notifications with read/unread state
- WebSocket notification delivery
- Dashboard summary, charts, approvals, activity feed, and AI-style summary
- Razorpay and Stripe payment plan flows
- Request logging, rate limiting, pagination, and optional Redis cache

## API Overview

Authentication:
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/refresh`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `GET /auth/google`
- `GET /auth/google/callback`

Users:
- `GET /users/`
- `GET /users/assignable`
- `GET /users/{user_id}`

Tasks:
- `POST /tasks/`
- `POST /tasks/withdocument`
- `GET /tasks/`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `PATCH /tasks/{task_id}/assign`
- `PATCH /tasks/{task_id}/smart-assign`
- `PATCH /tasks/{task_id}/status`
- `GET /tasks/kanban`
- `GET /tasks/assignment/recommendation`

Kanban:
- `GET /kanban/board`
- `PATCH /kanban/tasks/{task_id}/status`

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

Documents:
- `POST /documents/upload?task_id={task_id}`
- `GET /documents/task/{task_id}`
- `GET /documents/{document_id}`

Activity, audit, notifications, and realtime:
- `GET /activity/`
- `GET /audit-logs/`
- `GET /notifications/`
- `PATCH /notifications/{notification_id}/read`
- `WS /ws/{user_id}`

Payments:
- `POST /payments/create-payment`
- `POST /payments/verify`
- `GET /payments/subscription`

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

Update `backend/.env` before running the API. The `.env` file is ignored by Git; commit changes to `backend/.env.example` when defaults need to be shared.

Required local settings:

```env
SECRET_KEY=replace-this-with-a-long-random-secret
DATABASE_URL=postgresql://postgres:password@localhost/enterprisecollab
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
FRONTEND_URL=http://localhost:5173
```

Optional integrations:

```env
REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TTL_SECONDS=300
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Optional frontend API override:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Default URLs:
- Backend API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Frontend: `http://127.0.0.1:5173`

## Verification

Backend:

```bash
cd backend
python -m compileall app
python -m alembic current
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

## Submission Checklist

- GitHub repository
- Swagger/Postman API testing screenshots
- Frontend workflow screenshots
- README documentation
- Working backend and frontend integration
