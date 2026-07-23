"""Test OTP verification flow directly against the database."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP"

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

engine = create_engine(os.environ["DATABASE_URL"])
session = Session(engine)

# Find users
users = session.execute(
    text("SELECT user_code, email, email_verified, email_otp, email_otp_expiry FROM users ORDER BY user_code")
).fetchall()
print("=== USERS ===")
for u in users:
    print(f"  {u.user_code}: email={u.email}, verified={u.email_verified}, otp={u.email_otp}")

# Pick first student user
student_user = session.execute(
    text("SELECT u.user_code, u.email, u.role FROM users u JOIN student_profiles sp ON sp.user_id = u.user_code LIMIT 1")
).fetchone()
print(f"\n=== TESTING WITH STUDENT: {student_user.email} ===")

# Simulate send-login-otp
otp = "123456"
session.execute(
    text("UPDATE users SET email_otp = :otp, email_otp_expiry = :expiry WHERE email = :email"),
    {"otp": otp, "expiry": datetime.now(timezone.utc) + timedelta(minutes=10), "email": student_user.email}
)
session.commit()
print(f"  Set OTP={otp} for {student_user.email}")

# Now simulate verify-login-otp - get user with all attributes
user = session.execute(
    text("""
        SELECT u.user_code, u.email, u.role, u.email_otp, u.email_otp_expiry,
               u.last_login, u.login_count, u.phone, u.email_verified,
               u.admin_id, u.teacher_id, u.student_id,
               u.profile_photo, u.last_seen, u.device_token, u.failed_login_count,
               u.is_deleted, u.created_at, u.updated_at, u.created_by, u.updated_by,
               u.is_active
        FROM users u WHERE u.email = :email
    """),
    {"email": student_user.email}
).fetchone()

print(f"\n  Found user: code={user.user_code}, role={user.role}, email_otp={user.email_otp}")
print(f"  OTP match: {user.email_otp == otp}")
print(f"  Expiry: {user.email_otp_expiry}, now: {datetime.now(timezone.utc)}")
print(f"  Not expired: {user.email_otp_expiry > datetime.now(timezone.utc) if user.email_otp_expiry else 'N/A'}")

# Check profile
profile = session.execute(
    text("SELECT * FROM student_profiles WHERE user_id = :uid"),
    {"uid": user.user_code}
).fetchone()
print(f"\n  StudentProfile: {dict(profile._mapping) if profile else 'NOT FOUND'}")

# Check role enum value
print(f"  Role value: {user.role}")
print(f"  str role: {str(user.role)}")

# Now check the get_user_profile flow logic
print("\n=== SIMULATING get_user_profile ===")

# Student profile
sp = session.execute(
    text("SELECT student_id, student_name, admission_number, profile_photo FROM student_profiles WHERE user_id = :uid"),
    {"uid": user.user_code}
).fetchone()
if sp:
    print(f"  Student profile found: {dict(sp._mapping)}")
else:
    print("  Student profile NOT FOUND - this would cause profile_data['profile'] = None")

session.close()
print("\n✅ Test complete")
