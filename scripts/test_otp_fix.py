"""Test OTP verification flow via API."""
import os, sys, httpx, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8210"

# Find a student email from DB
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP"
from sqlalchemy import create_engine, text
engine = create_engine(os.environ["DATABASE_URL"])
conn = engine.connect()
user = conn.execute(
    text("SELECT email FROM users WHERE role = 'STUDENT' LIMIT 1")
).fetchone()
email = user.email
print(f"Using email: {email}")
conn.close()

# 1. Send login OTP
print("\n1. Sending login OTP...")
r = httpx.post(f"{BASE_URL}/send-login-otp", json={"email": email}, timeout=10)
print(f"   Status: {r.status_code}, Body: {r.json()}")

# 2. Read OTP from DB
time.sleep(1)
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP"
from sqlalchemy import create_engine, text
engine = create_engine(os.environ["DATABASE_URL"])
conn = engine.connect()
otp_row = conn.execute(
    text("SELECT email_otp FROM users WHERE email = :e"), {"e": email}
).fetchone()
otp = otp_row.email_otp
print(f"   OTP from DB: {otp}")
conn.close()

# 3. Verify login OTP
print("\n2. Verifying login OTP...")
r = httpx.post(f"{BASE_URL}/verify-login-otp", json={"email": email, "otp": otp}, timeout=10)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Access token: {data['access_token'][:30]}...")
    print(f"   User: {data['user']['email']}")
    print(f"   Profile: {data.get('profile')}")
else:
    print(f"   Error: {r.json()}")
