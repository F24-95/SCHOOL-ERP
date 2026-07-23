"""
Test data insertion and relationships with business_id PKs.
Creates sample data across all major tables and verifies FK relationships.
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

from datetime import date, time
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.database import Base
from app.core.enums import NoticeAudience, NoticeType, UserRole
from app.helpers.code_generators import *
from app.model import *

engine = create_engine("sqlite:///test_business_id.db", echo=False)
Base.metadata.create_all(bind=engine)

db = Session(bind=engine)

try:
    # ============================================================
    # 1. Create User (Admin)
    # ============================================================
    admin_user = User(
        business_id=generate_user_business_id(),
        email="admin@school.com",
        phone="9876543210",
        role=UserRole.ADMIN,
        password_hash="hashed_password",
    )
    db.add(admin_user)
    db.flush()
    print(f"1. Created Admin User: business_id={admin_user.business_id}")

    # Create AdminProfile (PK = admin_id, FK user_id -> users.business_id)
    admin_profile = AdminProfile(
        admin_id=generate_admin_code(),
        user_id=admin_user.business_id,
        admin_name="Principal Sir",
        super_admin=True,
    )
    db.add(admin_profile)
    db.flush()
    print(
        f"2. Created AdminProfile: admin_id={admin_profile.admin_id}, user_id={admin_profile.user_id}"
    )

    # ============================================================
    # 2. Academic Session
    # ============================================================
    session = AcademicSession(
        session_code="SES-2026",
        session_name="2026-27",
        start_year=2026,
        end_year=2027,
        start_date=date(2026, 4, 1),
        end_date=date(2027, 3, 31),
        is_current=True,
    )
    db.add(session)
    db.flush()
    print(f"3. Created AcademicSession: session_code={session.session_code}")

    # ============================================================
    # 3. ClassRoom + Subject + ClassSubject
    # ============================================================
    classroom = ClassRoom(
        class_code="CLS10A",
        class_name="Class 10",
        section="A",
        display_name="Class 10-A",
        academic_sessions_id=session.session_code,
        created_by=admin_user.business_id,
    )
    db.add(classroom)
    db.flush()
    print(f"4. Created ClassRoom: class_code={classroom.class_code}")

    subject = Subject(
        subject_code="MATH10",
        subject_name="Mathematics",
        created_by=admin_user.business_id,
    )
    db.add(subject)
    db.flush()
    print(f"5. Created Subject: subject_code={subject.subject_code}")

    class_subject = ClassSubject(
        business_id=generate_class_subject_id(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        subject_id=subject.subject_code,
        created_by=admin_user.business_id,
    )
    db.add(class_subject)
    db.flush()
    print(f"6. Created ClassSubject: business_id={class_subject.business_id}")

    # ============================================================
    # 4. Teacher User + TeacherProfile + TeacherSubject
    # ============================================================
    teacher_user = User(
        business_id=generate_user_business_id(),
        email="teacher@school.com",
        phone="9876543211",
        role=UserRole.TEACHER,
        password_hash="hashed_password",
        teacher_id=generate_teacher_id(1),
    )
    db.add(teacher_user)
    db.flush()

    teacher_profile = TeacherProfile(
        teacher_id=teacher_user.teacher_id,
        user_id=teacher_user.business_id,
        teacher_name="Math Teacher",
    )
    db.add(teacher_profile)
    db.flush()
    print(f"7. Created Teacher: teacher_id={teacher_profile.teacher_id}")

    teacher_subject = TeacherSubject(
        business_id=generate_teacher_subject_id(),
        academic_sessions_id=session.session_code,
        class_subject_id=class_subject.business_id,
        classroom_id=classroom.class_code,
        subject_id=subject.subject_code,
        teacher_id=teacher_profile.teacher_id,
    )
    db.add(teacher_subject)
    db.flush()
    print(f"8. Created TeacherSubject: business_id={teacher_subject.business_id}")

    # ============================================================
    # 5. Student User + StudentProfile + StudentClass
    # ============================================================
    student_user = User(
        business_id=generate_user_business_id(),
        email="student@school.com",
        phone="9876543212",
        role=UserRole.STUDENT,
        password_hash="hashed_password",
        student_id=generate_student_id(1),
    )
    db.add(student_user)
    db.flush()

    student_profile = StudentProfile(
        student_id=student_user.student_id,
        user_id=student_user.business_id,
        student_name="Test Student",
        school_name="Test School",
    )
    db.add(student_profile)
    db.flush()
    print(f"9. Created Student: student_id={student_profile.student_id}")

    student_class = StudentClass(
        business_id=generate_student_class_id(),
        academic_sessions_id=session.session_code,
        student_id=student_profile.student_id,
        classroom_id=classroom.class_code,
        roll_number=1,
        admission_date=date(2026, 4, 1),
    )
    db.add(student_class)
    db.flush()
    print(f"10. Created StudentClass: business_id={student_class.business_id}")

    # ============================================================
    # 6. TimeSlot + WeekDay + ClassTimeTable
    # ============================================================
    from app.model.timetable import (
        ClassTimeTable,
        TimeSlot,
        WeekDay,
    )

    weekday = WeekDay(day_code="MON", day_name="Monday", display_order=1)
    db.add(weekday)
    db.flush()

    timeslot = TimeSlot(
        slot_code="P1",
        slot_name="First Period",
        start_time=time(8, 0),
        end_time=time(9, 0),
        duration_minutes=60,
        display_order=1,
    )
    db.add(timeslot)
    db.flush()
    print("11. Created WeekDay+TimeSlot")

    timetable = ClassTimeTable(
        business_id=generate_uuid(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        class_subject_id=class_subject.business_id,
        teacher_subject_id=teacher_subject.business_id,
        week_day_id=weekday.day_code,
        time_slot_id=timeslot.slot_code,
    )
    db.add(timetable)
    db.flush()
    print(f"12. Created ClassTimeTable: business_id={timetable.business_id}")

    # ============================================================
    # 7. Assignment + AssignmentResult
    # ============================================================
    assignment = Assignment(
        business_id=generate_assignment_id(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        class_subject_id=class_subject.business_id,
        teacher_subject_id=teacher_subject.business_id,
        title="Test Assignment",
        due_date=date(2026, 8, 1),
        total_marks=100,
        passing_marks=40,
        created_by=teacher_user.business_id,
    )
    db.add(assignment)
    db.flush()
    print(f"13. Created Assignment: business_id={assignment.business_id}")

    assignment_result = AssignmentResult(
        business_id=generate_assignment_result_id(),
        assignment_id=assignment.business_id,
        student_class_id=student_class.business_id,
        obtained_marks=85,
    )
    db.add(assignment_result)
    db.flush()
    print(f"14. Created AssignmentResult: business_id={assignment_result.business_id}")

    # ============================================================
    # 8. Exam + ExamResult
    # ============================================================
    exam = Exam(
        business_id=generate_exam_code(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        class_subject_id=class_subject.business_id,
        teacher_subject_id=teacher_subject.business_id,
        exam_name="Mid Term",
        exam_type="Written",
        exam_date=date(2026, 9, 15),
        total_marks=100,
        passing_marks=40,
        created_by=teacher_user.business_id,
    )
    db.add(exam)
    db.flush()
    print(f"15. Created Exam: business_id={exam.business_id}")

    exam_result = ExamResult(
        business_id=generate_exam_result_id(),
        exam_id=exam.business_id,
        student_class_id=student_class.business_id,
        obtained_marks=90,
    )
    db.add(exam_result)
    db.flush()
    print(f"16. Created ExamResult: business_id={exam_result.business_id}")

    # ============================================================
    # 9. Fee
    # ============================================================
    from decimal import Decimal

    fee = Fee(
        business_id=generate_fee_code(),
        academic_sessions_id=session.session_code,
        student_class_id=student_class.business_id,
        fee_month=7,
        fee_year=2026,
        total_amount=Decimal("5000.00"),
        paid_amount=Decimal("5000.00"),
        due_date=date(2026, 7, 15),
        created_by=admin_user.business_id,
    )
    db.add(fee)
    db.flush()
    print(f"17. Created Fee: business_id={fee.business_id}")

    # ============================================================
    # 10. Notice
    # ============================================================
    from app.core.enums import NoticeAudience, NoticeType

    notice = Notice(
        business_id=generate_notice_code(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        title="School Holiday",
        description="Tomorrow is a holiday",
        notice_type=NoticeType.GENERAL,
        audience=NoticeAudience.ALL,
        publish_date=date(2026, 7, 20),
        created_by=admin_user.business_id,
    )
    db.add(notice)
    db.flush()
    print(f"18. Created Notice: business_id={notice.business_id}")

    # ============================================================
    # 19. StudyMaterial
    # ============================================================
    material = StudyMaterial(
        business_id=generate_material_id(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        class_subject_id=class_subject.business_id,
        teacher_subject_id=teacher_subject.business_id,
        title="Chapter 1 Notes",
        material_type="PDF",
        file_name="ch1.pdf",
        file_url="/uploads/ch1.pdf",
        uploaded_by=teacher_user.business_id,
    )
    db.add(material)
    db.flush()
    print(f"19. Created StudyMaterial: business_id={material.business_id}")

    # ============================================================
    # 20. ChatRoom + ChatMessage
    # ============================================================
    chat_room = ChatRoom(
        business_id=generate_chat_room_id(),
        academic_sessions_id=session.session_code,
        student_class_id=student_class.business_id,
        teacher_subject_id=teacher_subject.business_id,
    )
    db.add(chat_room)
    db.flush()
    print(f"20. Created ChatRoom: business_id={chat_room.business_id}")

    chat_msg = ChatMessage(
        business_id=generate_chat_message_id(),
        chat_room_id=chat_room.business_id,
        sender_id=teacher_user.business_id,
        message="Hello class!",
    )
    db.add(chat_msg)
    db.flush()
    print(f"21. Created ChatMessage: business_id={chat_msg.business_id}")

    # ============================================================
    # 22. DailyClass + DailyClassStudent + StudentAttendance
    # ============================================================
    daily_class = DailyClass(
        business_id=generate_uuid(),
        academic_sessions_id=session.session_code,
        classroom_id=classroom.class_code,
        class_subject_id=class_subject.business_id,
        teacher_subject_id=teacher_subject.business_id,
        timetable_id=timetable.business_id,
        class_date=date(2026, 7, 20),
    )
    db.add(daily_class)
    db.flush()
    print(f"22. Created DailyClass: business_id={daily_class.business_id}")

    dcs = DailyClassStudent(
        business_id=generate_uuid(),
        daily_class_id=daily_class.business_id,
        student_class_id=student_class.business_id,
        attendance_status="Present",
        marked_by=teacher_user.business_id,
    )
    db.add(dcs)
    db.flush()
    print(f"23. Created DailyClassStudent: business_id={dcs.business_id}")

    attendance = StudentAttendance(
        business_id=generate_uuid(),
        student_class_id=student_class.business_id,
        total_classes=1,
        present_classes=1,
    )
    db.add(attendance)
    db.flush()
    print(f"24. Created StudentAttendance: business_id={attendance.business_id}")

    # ============================================================
    # VERIFY RELATIONSHIPS (Queries)
    # ============================================================
    print("\n=== VERIFYING RELATIONSHIPS ===")

    # User -> Profile
    u = db.query(User).filter(User.business_id == admin_user.business_id).first()
    assert u.admin_profile is not None, "Admin profile relationship broken!"
    assert u.admin_profile.user_id == u.business_id
    print("25. User->AdminProfile: OK")

    # Teacher -> TeacherSubject -> ClassSubject -> ClassRoom
    ts = (
        db.query(TeacherSubject)
        .filter(TeacherSubject.business_id == teacher_subject.business_id)
        .first()
    )
    assert ts.teacher is not None
    assert ts.classroom is not None
    assert ts.subject is not None
    assert ts.class_subject is not None
    print("26. TeacherSubject relationships: OK")

    # Student -> StudentClass
    sc = (
        db.query(StudentClass)
        .filter(StudentClass.business_id == student_class.business_id)
        .first()
    )
    assert sc.student is not None
    assert sc.classroom is not None
    print("27. StudentClass relationships: OK")

    # Assignment -> Results
    a = (
        db.query(Assignment)
        .filter(Assignment.business_id == assignment.business_id)
        .first()
    )
    assert len(a.results) == 1
    assert a.results[0].business_id == assignment_result.business_id
    print("28. Assignment->AssignmentResult: OK")

    # Exam -> Results
    e = db.query(Exam).filter(Exam.business_id == exam.business_id).first()
    assert len(e.results) == 1
    print("29. Exam->ExamResult: OK")

    # ChatRoom -> Messages
    cr = (
        db.query(ChatRoom).filter(ChatRoom.business_id == chat_room.business_id).first()
    )
    assert len(cr.messages) == 1
    print("30. ChatRoom->ChatMessage: OK")

    # DailyClass -> Students
    dc = (
        db.query(DailyClass)
        .filter(DailyClass.business_id == daily_class.business_id)
        .first()
    )
    assert len(dc.students) == 1
    print("31. DailyClass->DailyClassStudent: OK")

    # ClassTimeTable -> WeekDay + TimeSlot
    tt = (
        db.query(ClassTimeTable)
        .filter(ClassTimeTable.business_id == timetable.business_id)
        .first()
    )
    assert tt.week_day is not None
    assert tt.time_slot is not None
    print("32. ClassTimeTable->WeekDay+TimeSlot: OK")

    # Committing all changes
    db.commit()
    print("\n=== ALL RELATIONSHIPS VERIFIED ===")
    print("### DATA INSERTION AND RELATIONSHIP TEST PASSED ###")

finally:
    db.close()
