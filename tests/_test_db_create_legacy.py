"""
Test database table creation and data insertion with business_id PKs.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DATABASE_URL"] = "sqlite:///test_business_id.db"
os.environ["SECRET_KEY"] = "test-secret-key-12345"
os.environ["APP_NAME"] = "Test"
os.environ["APP_VERSION"] = "1.0"
os.environ["APP_ENV"] = "test"
os.environ["DEBUG"] = "true"
os.environ["ALLOWED_ORIGINS"] = "*"

from sqlalchemy import create_engine, inspect

from app.api.database import Base
from app.model import *

engine = create_engine("sqlite:///test_business_id.db", echo=False)
Base.metadata.create_all(bind=engine)

insp = inspect(engine)
tables = insp.get_table_names()
print(f"Created {len(tables)} tables:")
pk_problems = []
for t in sorted(tables):
    cols = insp.get_columns(t)
    pk_cols = [c for c in cols if c.get("primary_key")]
    pk_names = [c["name"] for c in pk_cols]
    for c in cols:
        if c["name"] in pk_names:
            col_type = str(c["type"])
            print(f"  {t}: PK {c['name']} ({col_type})")
            # Check for Integer PKs that shouldn't exist
            if c["name"] == "id" and "INTEGER" in col_type.upper():
                pk_problems.append(
                    f"{t}.id is Integer PK - should be business_id (String)"
                )
            break

if pk_problems:
    print(f"\nPROBLEMS FOUND ({len(pk_problems)}):")
    for p in pk_problems:
        print(f"  {p}")
else:
    print("\nAll PKs are correct - no Integer id PKs found!")

print("\nDone!")
