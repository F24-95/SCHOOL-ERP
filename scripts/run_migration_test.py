"""Run alembic upgrade against SCHOOL_ERP_TEST database."""

import os
import sys

# Override to test database
os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP_TEST"
)
os.environ["DATABASE_NAME"] = "SCHOOL_ERP_TEST"
os.environ["APP_ENV"] = "test"
os.environ["DEBUG"] = "true"
os.environ["SECRET_KEY"] = "test-secret-key-12345"
os.environ["ALLOWED_ORIGINS"] = "*"
os.environ["SMTP_SERVER"] = "localhost"
os.environ["SMTP_PORT"] = "1025"
os.environ["SMTP_EMAIL"] = "test@test.com"
os.environ["SMTP_PASSWORD"] = "test"
os.environ["FRONTEND_URL"] = "http://localhost:3000"
os.environ["UPLOAD_DIR"] = "test_uploads"
os.environ["LOG_LEVEL"] = "CRITICAL"

# Now run alembic upgrade
from alembic.config import CommandLine

sys.argv = ["alembic", "upgrade", "head"]
CommandLine().main()
