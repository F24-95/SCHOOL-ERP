"""Create SCHOOL_ERP_TEST database for testing."""

import psycopg

conn = psycopg.connect(
    "host=localhost port=5432 dbname=postgres user=postgres password=Faizan9517"
)
conn.autocommit = True
cur = conn.cursor()
# Terminate any existing connections
cur.execute("""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'SCHOOL_ERP_TEST'
      AND pid <> pg_backend_pid()
""")
cur.execute('DROP DATABASE IF EXISTS "SCHOOL_ERP_TEST"')
cur.execute('CREATE DATABASE "SCHOOL_ERP_TEST"')
cur.close()
conn.close()
print("SCHOOL_ERP_TEST created OK")
