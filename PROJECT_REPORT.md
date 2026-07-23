# PROJECT REPORT - SCHOOL ERP

## Overview
This project is a School ERP backend built with FastAPI and SQLAlchemy.

---

## Architecture

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (async-ready)
- **Database**: PostgreSQL
- **Auth**: JWT-based with role-based access control (Admin, Teacher, Student)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Search**: RapidFuzz for fuzzy matching with in-memory TTL cache

---

## Project Structure

```
SCHOOL-ERP/
├── app/
│   ├── main.py              # Entry point - CORS, middleware, router registration
│   ├── api/
│   │   ├── config.py        # Pydantic Settings (env-based)
│   │   └── database.py      # Engine, SessionLocal, get_db dependency
│   ├── model/               # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routers/             # API route handlers (thin - delegate to services)
│   ├── services/            # Business logic layer
│   ├── repositories/        # Data access layer (DB queries)
│   ├── helpers/             # Shared utilities (search engine, caching, code generators)
│   ├── core/                # Enums, constants
│   └── validators/          # Input validation
├── alembic/                 # Migration configuration and version files
├── uploads/                 # File uploads directory
├── .env                     # Environment variables (git-ignored)
├── .env.example             # Template for environment variables
├── aboutapi.md              # API documentation
└── PROJECT_REPORT.md        # This file
```

---

## Database Schema

### Core Tables
- `users` - Authentication and base user info (id, email, phone, role, password_hash)
- `student_profiles` - Student-specific data (student_id, student_name, registration_number, etc.)
- `teacher_profiles` - Teacher-specific data (teacher_id, teacher_name, department, etc.)
- `admin_profiles` - Admin-specific data (admin_id, admin_name, etc.)

### Academic Tables
- `academic_sessions` - School sessions/years (session_code, start_date, end_date, is_current)
- `class_rooms` - Class/section definitions (class_code, class_name, section, display_name)
- `subjects` - Subject definitions (subject_code, subject_name, subject_type)
- `class_subjects` - Subject-class mappings
- `teacher_subjects` - Teacher-subject assignments (across sessions, classrooms)
- `student_classes` - Student enrollment in classes (roll_number, admission_date, status)

### Feature Tables
- `notices` - Announcements and notices
- `assignments` - Student assignments
- `exams` - Examination schedules and results
- `fees` - Fee records and payments
- `attendance` - Daily attendance tracking
- `timetables` - Class timetables
- `study_materials` - Learning resources
- `zoom_meetings` - Zoom integration data
- `chat_messages` - Internal messaging
- `topics` / `courses` - Course/topic management

---

## API Endpoints

See `aboutapi.md` for complete API documentation with access roles and request data requirements.

### Admin Routes (`/admin/*`)
- User CRUD (create, list, get, update, delete)
- Admin Profile list
- Academic Session CRUD
- Classroom CRUD
- Subject CRUD
- Teacher-Subject mapping
- Student-Class enrollment
- Flat profile lists (students, teachers)
- System health check
- System statistics

### Auth Routes (`/auth/*`)
- Login, Register, Token refresh
- Forgot/Reset password
- Email verification

### Student Routes (`/students/*`)
- Profile management
- Assignment submission
- Fee history
- Attendance view
- Timetable view

### Teacher Routes (`/teachers/*`)
- Profile management
- Assignment creation/grading
- Attendance marking
- Exam management

### Search Routes
- `GET /students/search` - Student search with RapidFuzz (cached)
- `GET /teachers/search` - Teacher search with RapidFuzz (cached)
- `GET /search/universal` - Cross-entity search
- `GET /search/classrooms` - Classroom search
- `GET /search/notices` - Notice search
- `GET /search/subjects` - Subject search

---

## Fixes Applied

### 1. Alembic Migrations
- **Problem**: Tables were created via `Base.metadata.create_all()` in `main.py` instead of Alembic migrations. Missing columns were added via `ensure_missing_columns()` which ran raw ALTER TABLE queries.
- **Fix**: 
  - Created initial migration at `alembic/versions/001_initial_schema.py` covering all 30+ tables with proper upgrade/downgrade.
  - Removed `Base.metadata.create_all(bind=engine)` from `app/main.py`.
  - Removed `ensure_missing_columns()` from `app/main.py`.
  - **Files changed**: `app/main.py`, `alembic/versions/001_initial_schema.py`

### 2. CORS Configuration
- **Problem**: CORS was set to `allow_origins=["*"]` allowing any origin to access the API.
- **Fix**: Replaced wildcard origin with config-driven `ALLOWED_ORIGINS` read from environment variable (via `app/api/config.py`), defaulting to `http://localhost:3000`.
- **Files changed**: `app/main.py`, `app/api/config.py`, `.env.example`

### 3. Direct DB Queries in Routers
- **Problem**: `app/routers/admin_router.py` contained inline SQLAlchemy queries and business logic directly in route handlers instead of using service classes.
- **Fix**: Created `app/services/admin_service.py` with dedicated service classes:
  - `AdminUserService` - User CRUD operations
  - `AdminProfileService` - Admin profile listing
  - `AcademicSessionService` - Session management
  - `ClassroomService` - Classroom management
  - `SubjectService` - Subject management
  - `TeacherSubjectService` - Teacher-subject assignments
  - `StudentClassService` - Student enrollment
  - `AdminStatsService` - System statistics
  - Router endpoints now instantiate these services and delegate all logic to them.
  - **Files changed**: `app/routers/admin_router.py`, `app/services/admin_service.py` (new)

### 4. Plaintext Password in .env
- **Problem**: `.env` file contained `DATABASE_PASSWORD=Faizan9517` and `SMTP_PASSWORD` in plaintext. File was tracked in git.
- **Fix**: 
  - Created `.env.example` with placeholder values as a committed template.
  - Removed `.env` from git tracking with `git rm --cached .env`.
  - `.env` remains in `.gitignore`.
  - **Files changed**: `.env.example` (new), `.env` (untracked)

### 5. Search Performance
- **Problem**: Fuzzy search (RapidFuzz) loaded all candidates from the database on every request - full table scans for every search query.
- **Fix**: Added `app/helpers/cache.py` with a thread-safe in-memory TTL cache (60s default). Search services (`student_search_service.py`, `teacher_search_service.py`) now cache fuzzy name/email pools and reuse them across requests.
- **Files changed**: `app/helpers/cache.py` (new), `app/services/search/student_search_service.py`, `app/services/search/teacher_search_service.py`

---

## Security Considerations

1. **Authentication**: JWT-based tokens with configurable expiry (`ACCESS_TOKEN_EXPIRE_MINUTES`).
2. **Authorization**: Role-based access control via `require_role()` dependency - endpoints restrict access to Admin, Teacher, or Student roles as appropriate.
3. **Password Storage**: Passwords hashed before storage.
4. **CORS**: Restricted to configured origins (default: `http://localhost:3000`).
5. **Environment Variables**: Secrets managed via `.env` (git-ignored). Template available in `.env.example`.
6. **Migrations**: Schema changes managed through Alembic, not raw SQL in application code.

---

## Service Layer Architecture

```
Router (thin)
  │
  ▼
Service (business logic, orchestration)
  │
  ▼
Repository (data access / DB queries)
```

All DB queries in `app/routers/` have been migrated to service classes. Exceptions (kept for simplicity):
- Flat profile list endpoints in admin_router.py (trivial queries)
- Unified search endpoints in unified_search_router.py (single-use ILIKE queries)

---

## Search Architecture

Two search strategies are in use:
1. **RapidFuzz Fuzzy Search** (students, teachers): Loads candidate pools, applies `fuzz.WRatio` scoring, ranks results. Candidate pools are now cached in memory with a 60-second TTL.
2. **ILIKE Pattern Search** (universal, classrooms, notices, subjects): Standard PostgreSQL `ILIKE` queries bounded by `LIMIT`. No caching needed as these are already efficient.

---

## Recent Activities

- [2026-07-20] Fixed all 5 identified issues (Alembic, CORS, direct DB queries, .env password, search caching)
- [2026-07-20] Created comprehensive API documentation (aboutapi.md)
- [2026-07-20] Generated initial Alembic migration
- [2026-07-20] Refactored admin_router.py - moved all inline DB queries to service classes
- [2026-07-20] Added in-memory caching for RapidFuzz search pools
- [2026-07-20] Created .env.example and removed .env from git tracking
