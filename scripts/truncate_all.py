import os
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP"
from sqlalchemy import create_engine, text
e = create_engine(os.environ["DATABASE_URL"])
conn = e.connect()
conn.execute(text("SET session_replication_role = replica"))
rs = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
tables = [r[0] for r in rs]
for t in tables:
    conn.execute(text(f'TRUNCATE TABLE "{t}" CASCADE'))
conn.execute(text("SET session_replication_role = DEFAULT"))
conn.commit()
conn.close()
print(f"Truncated {len(tables)} tables")
