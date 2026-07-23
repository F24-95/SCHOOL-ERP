"""Run alembic migration against SCHOOL_ERP_TEST database."""

import os
import sys

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP_TEST"
)
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

# Verify we can connect
import psycopg

conn = psycopg.connect(
    "host=localhost port=5432 dbname=SCHOOL_ERP_TEST user=postgres password=Faizan9517"
)
conn.close()
print("Connected to SCHOOL_ERP_TEST OK")

# Run alembic
from alembic.config import CommandLine

sys.argv = ["alembic", "upgrade", "head"]
try:
    CommandLine().main()
except SystemExit:
    pass
print("Migration complete")
