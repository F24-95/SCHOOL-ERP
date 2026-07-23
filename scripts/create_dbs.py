import psycopg

conn = psycopg.connect("postgresql://postgres:Faizan9517@localhost:5432/postgres")
conn.autocommit = True
cur = conn.cursor()

for db_name in ["SCHOOL_ERP", "SCHOOL_ERP_TEST"]:
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
    if cur.fetchone():
        cur.execute('DROP DATABASE "{}"'.format(db_name))
        print("Dropped", db_name)
    cur.execute('CREATE DATABASE "{}"'.format(db_name))
    print("Created", db_name)

cur.close()
conn.close()
