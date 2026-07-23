import os

# ── Must be set BEFORE any app imports ──────────────────────────────────
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP_TEST",
)
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-12345")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ.setdefault("APP_NAME", "Test")
os.environ.setdefault("APP_VERSION", "1.0")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("ALLOWED_ORIGINS", "*")
os.environ.setdefault("SMTP_SERVER", "localhost")
os.environ.setdefault("SMTP_PORT", "1025")
os.environ.setdefault("SMTP_EMAIL", "test@test.com")
os.environ.setdefault("SMTP_PASSWORD", "test")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("UPLOAD_DIR", "test_uploads")
os.environ.setdefault("LOG_LEVEL", "CRITICAL")

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.config import settings
from app.api.database import Base, get_db
from app.auth import create_access_token, hash_password
from app.core.enums import (
    UserRole,
)
from app.dependencies import get_current_user
from app.helpers.code_generators import (
    generate_admin_code,
    generate_class_subject_id,
    generate_student_class_id,
    generate_student_id,
    generate_teacher_id,
    generate_teacher_subject_id,
    generate_user_business_id,
)
from app.main import app
from app.model import (
    AcademicSession,
    AdminProfile,
    ClassRoom,
    ClassSubject,
    StudentClass,
    StudentProfile,
    Subject,
    TeacherProfile,
    TeacherSubject,
    User,
)

TEST_DB_URL = settings.DATABASE_URL
engine = create_engine(TEST_DB_URL, pool_pre_ping=True, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ── Session-scoped: create schema (isolated test infra via create_all) ──
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


# ── Per-test: transaction rollback isolation ───────────────────────────
@pytest.fixture
def db_session(setup_database):
    # Re-create all tables in case another concurrent test process
    # has called drop_all() at session-end, which would leave table
    # objects missing for this test run.
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    old_override = app.dependency_overrides.get(get_db)

    def _override():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = _override
    yield session
    app.dependency_overrides[get_db] = old_override
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    return TestClient(app)


# ── User fixtures ──────────────────────────────────────────────────────


@pytest.fixture
def admin_user(db_session):
    business_id = generate_user_business_id()
    admin_id_val = generate_admin_code()
    user = User(
        business_id=business_id,
        email="admin@test.edu",
        phone="9876543210",
        role=UserRole.ADMIN,
        password_hash=hash_password("admin@123"),
        admin_id=admin_id_val,
        email_verified=True,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    profile = AdminProfile(
        admin_id=admin_id_val,
        user_id=business_id,
        admin_name="Test Admin",
        super_admin=True,
        can_create_admin=True,
    )
    db_session.add(profile)
    db_session.flush()
    return user


@pytest.fixture
def teacher_user(db_session):
    business_id = generate_user_business_id()
    tid = generate_teacher_id(1)
    user = User(
        business_id=business_id,
        email="teacher@test.edu",
        phone="9876543211",
        role=UserRole.TEACHER,
        password_hash=hash_password("teacher@123"),
        teacher_id=tid,
        email_verified=True,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    profile = TeacherProfile(
        teacher_id=tid,
        user_id=business_id,
        teacher_name="Test Teacher",
        designation="Senior Teacher",
        department="Science",
        employee_code="EMP001",
    )
    db_session.add(profile)
    db_session.flush()
    return user


@pytest.fixture
def student_user(db_session):
    business_id = generate_user_business_id()
    sid = generate_student_id(1)
    user = User(
        business_id=business_id,
        email="student@test.edu",
        phone="9876543212",
        role=UserRole.STUDENT,
        password_hash=hash_password("student@123"),
        student_id=sid,
        email_verified=True,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    profile = StudentProfile(
        student_id=sid,
        user_id=business_id,
        student_name="Test Student",
        school_name="Test School",
    )
    db_session.add(profile)
    db_session.flush()
    return user


# ── Academic fixtures ──────────────────────────────────────────────────


@pytest.fixture
def academic_session(db_session, admin_user):
    obj = AcademicSession(
        session_code="SES-2026",
        session_name="2026-27",
        start_year=2026,
        end_year=2027,
        start_date=date(2026, 4, 1),
        end_date=date(2027, 3, 31),
        is_current=True,
        created_by=admin_user.business_id,
    )
    db_session.add(obj)
    db_session.flush()
    return obj


@pytest.fixture
def classroom(db_session, academic_session, admin_user):
    cls = ClassRoom(
        class_code="CLS10A",
        class_name="Class 10",
        section="A",
        display_name="Class 10-A",
        academic_sessions_id=academic_session.session_code,
        created_by=admin_user.business_id,
    )
    db_session.add(cls)
    db_session.flush()
    return cls


@pytest.fixture
def subject(db_session, admin_user):
    subj = Subject(
        subject_code="MATH10",
        subject_name="Mathematics",
        subject_type="Core",
        created_by=admin_user.business_id,
    )
    db_session.add(subj)
    db_session.flush()
    return subj


@pytest.fixture
def class_subject(db_session, academic_session, classroom, subject, admin_user):
    cs = ClassSubject(
        business_id=generate_class_subject_id(),
        academic_sessions_id=academic_session.session_code,
        classroom_id=classroom.class_code,
        subject_id=subject.subject_code,
        created_by=admin_user.business_id,
    )
    db_session.add(cs)
    db_session.flush()
    return cs


@pytest.fixture
def teacher_subject(
    db_session, academic_session, classroom, subject, class_subject, teacher_user
):
    ts = TeacherSubject(
        business_id=generate_teacher_subject_id(),
        academic_sessions_id=academic_session.session_code,
        class_subject_id=class_subject.business_id,
        classroom_id=classroom.class_code,
        subject_id=subject.subject_code,
        teacher_id=teacher_user.teacher_id,
    )
    db_session.add(ts)
    db_session.flush()
    return ts


@pytest.fixture
def student_class(db_session, academic_session, classroom, student_user):
    sc = StudentClass(
        business_id=generate_student_class_id(),
        academic_sessions_id=academic_session.session_code,
        student_id=student_user.student_id,
        classroom_id=classroom.class_code,
        roll_number=1,
        admission_date=date(2026, 4, 1),
    )
    db_session.add(sc)
    db_session.flush()
    return sc


# ── Override fixtures (dependency injection) ───────────────────────────


@pytest.fixture
def override_admin(admin_user):
    app.dependency_overrides[get_current_user] = lambda: admin_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def override_teacher(teacher_user):
    app.dependency_overrides[get_current_user] = lambda: teacher_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def override_student(student_user):
    app.dependency_overrides[get_current_user] = lambda: student_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


# ── Token fixtures ─────────────────────────────────────────────────────


@pytest.fixture
def admin_token(admin_user):
    return create_access_token({"sub": admin_user.business_id, "role": "admin"})


@pytest.fixture
def teacher_token(teacher_user):
    return create_access_token({"sub": teacher_user.business_id, "role": "teacher"})


@pytest.fixture
def student_token(student_user):
    return create_access_token({"sub": student_user.business_id, "role": "student"})


@pytest.fixture
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def auth_headers_teacher(teacher_token):
    return {"Authorization": f"Bearer {teacher_token}"}


@pytest.fixture
def auth_headers_student(student_token):
    return {"Authorization": f"Bearer {student_token}"}


@pytest.fixture
def seed_all(
    db_session,
    admin_user,
    teacher_user,
    student_user,
    academic_session,
    classroom,
    subject,
    class_subject,
    teacher_subject,
    student_class,
):
    pass
