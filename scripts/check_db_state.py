"""Check SCHOOL_ERP database state."""

import psycopg

c = psycopg.connect(
    "host=localhost port=5432 dbname=SCHOOL_ERP user=postgres password=Faizan9517"
)
cur = c.cursor()
cur.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
)
tables = [t[0] for t in cur.fetchall()]
print(f"Tables ({len(tables)}):")
for t in tables:
    print(f"  - {t}")
try:
    cur.execute("SELECT * FROM alembic_version")
    print(f"Alembic version: {cur.fetchall()}")
except Exception as e:
    print(f"No alembic_version table: {e}")
c.close()
