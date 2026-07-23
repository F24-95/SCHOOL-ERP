"""Check key table schemas in SCHOOL_ERP."""

import psycopg

c = psycopg.connect(
    "host=localhost port=5432 dbname=SCHOOL_ERP user=postgres password=Faizan9517"
)
cur = c.cursor()

tables = [
    "users",
    "academic_sessions",
    "classroom",
    "subjects",
    "assignments",
    "student_profiles",
    "teacher_profiles",
    "admin_profiles",
]
for table in tables:
    cur.execute(
        f"SELECT column_name, data_type, character_maximum_length, is_nullable, column_default FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position"
    )
    cols = cur.fetchall()
    print(f"\n=== {table} ===")
    for col in cols:
        print(
            f"  {col[0]:25s} {col[1]:15s} len={col[2]!s:5s} nullable={col[3]} default={col[4]!s:30s}"
        )

    # Check PK
    cur.execute(
        f"SELECT kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name WHERE tc.table_name = '{table}' AND tc.constraint_type = 'PRIMARY KEY'"
    )
    pks = [r[0] for r in cur.fetchall()]
    print(f"  PK: {pks}")

c.close()
