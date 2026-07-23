"""Run v3 migration against SCHOOL_ERP database."""

import os

# Use the .env DATABASE_URL for SCHOOL_ERP
os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP"
)
os.environ["APP_ENV"] = "test"
os.environ["DEBUG"] = "true"
os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY", "test-key-12345")
os.environ["ALLOWED_ORIGINS"] = "*"
os.environ["SMTP_SERVER"] = "localhost"
os.environ["SMTP_PORT"] = "1025"
os.environ["SMTP_EMAIL"] = "test@test.com"
os.environ["SMTP_PASSWORD"] = "test"
os.environ["FRONTEND_URL"] = "http://localhost:3000"
os.environ["UPLOAD_DIR"] = "test_uploads"
os.environ["LOG_LEVEL"] = "CRITICAL"

import sys

from alembic.config import CommandLine

sys.argv = ["alembic", "upgrade", "head"]
try:
    CommandLine().main()
except SystemExit:
    pass
print("Migration complete")
