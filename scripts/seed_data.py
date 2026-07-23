"""Seed 5-10 records into every table to verify all models, FKs & relationships."""

import os
import sys
from datetime import date, datetime, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:Faizan9517@localhost:5432/SCHOOL_ERP"

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

from app.api.database import Base
from app.core.enums import (
    AssignmentStatus, ExamStatus, FeeStatus, MaterialType,
    NoticeAudience, NoticeType, UserRole,
)
from app.helpers.code_generators import (
    generate_admin_code, generate_assignment_code, generate_assignment_result_code,
    generate_attachment_code, generate_attendance_code, generate_availability_code,
    generate_chat_message_code, generate_chat_room_code, generate_class_subject_code,
    generate_daily_class_code, generate_daily_class_student_code, generate_duration_report_code,
    generate_exam_code, generate_exam_result_code, generate_fee_code,
    generate_id_card_code, generate_interaction_report_code, generate_ka_course_code,
    generate_ka_student_code, generate_material_code, generate_notice_code,
    generate_promotion_code, generate_report_code, generate_student_class_code,
    generate_teacher_subject_code, generate_timetable_code, generate_topic_code,
    generate_topic_progress_code, generate_topic_progress_report_code, generate_user_code,
    generate_zoom_file_code, generate_zoom_interaction_code,
    generate_zoom_transcript_code, random_code,
)
from app.model import *

engine = create_engine(os.environ["DATABASE_URL"], echo=False)
session = Session(engine)

created = {}  # track created objects by type


def flush():
    session.flush()


# ═══════════════════════════════════════════════════════
# 1. ACADEMIC SESSIONS
# ═══════════════════════════════════════════════════════
sessions = []
for y in range(2023, 2027):
    s = AcademicSession(
        session_code=f"SES-{y}",
        session_name=f"{y}-{str(y+1)[-2:]}",
        start_year=y,
        end_year=y + 1,
        start_date=date(y, 4, 1),
        end_date=date(y + 1, 3, 31),
        is_current=(y == 2026),
    )
    session.add(s)
    sessions.append(s)
flush()
created["academic_sessions"] = sessions
print(f"✓ academic_sessions: {len(sessions)} rows")

# ═══════════════════════════════════════════════════════
# 2. USERS
# ═══════════════════════════════════════════════════════
users = []
roles = [UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT]
for i in range(1, 11):
    u = User(
        user_code=generate_user_code(),
        email=f"user{i}@school.edu",
        phone=f"987654{i:03d}0",
        password_hash="dummy_hash",
        role=roles[i % 3],
        email_verified=True,
        is_active=True,
    )
    session.add(u)
    users.append(u)
flush()
created["users"] = users
print(f"✓ users: {len(users)} rows")

# ═══════════════════════════════════════════════════════
# 3. PROFILES
# ═══════════════════════════════════════════════════════
admins, teachers, students = [], [], []
for u in users:
    if u.role == UserRole.ADMIN:
        aid = generate_admin_code()
        u.admin_id = aid  # FK target for AdminProfile.admin_id
        p = AdminProfile(admin_id=aid, user_id=u.user_code, admin_name=f"Admin{u.user_code[-4:]}", super_admin=True)
        session.add(p); admins.append(p)
    elif u.role == UserRole.TEACHER:
        tid = f"TCH{random_code(8)}"
        u.teacher_id = tid  # FK target for TeacherProfile.teacher_id
        p = TeacherProfile(teacher_id=tid, user_id=u.user_code, teacher_name=f"Teacher{u.user_code[-4:]}")
        session.add(p); teachers.append(p)
    elif u.role == UserRole.STUDENT:
        sid = f"STU{random_code(8)}"
        u.student_id = sid  # FK target for StudentProfile.student_id
        p = StudentProfile(student_id=sid, user_id=u.user_code, student_name=f"Student{u.user_code[-4:]}",
                           school_name="Test School")
        session.add(p); students.append(p)
flush()
created["admin_profiles"] = admins
created["teacher_profiles"] = teachers
created["student_profiles"] = students
print(f"✓ profiles: {len(admins)} admin, {len(teachers)} teacher, {len(students)} student")

# ═══════════════════════════════════════════════════════
# 4. CLASSROOM
# ═══════════════════════════════════════════════════════
classrooms = []
for i, cls_name in enumerate(["Class 1", "Class 5", "Class 9", "Class 10", "Class 12"]):
    section = ["A", "B", "C", "D", "COM"][i]
    code = f"CLS{cls_name.replace('Class ','')}{section}"
    c = ClassRoom(
        class_code=code, class_name=cls_name, section=section,
        display_name=f"{cls_name}-{section}",
        academic_sessions_id=sessions[-1].session_code,
        created_by=users[0].user_code,
    )
    session.add(c)
    classrooms.append(c)
flush()
created["classrooms"] = classrooms
print(f"✓ classrooms: {len(classrooms)} rows")

# ═══════════════════════════════════════════════════════
# 5. SUBJECTS
# ═══════════════════════════════════════════════════════
subjects = []
for name, code in [("Mathematics", "MATH"), ("Science", "SCI"), ("English", "ENG"),
                   ("Hindi", "HIN"), ("Computer Science", "CS")]:
    s = Subject(subject_code=code, subject_name=name, created_by=users[0].user_code)
    session.add(s)
    subjects.append(s)
flush()
created["subjects"] = subjects
print(f"✓ subjects: {len(subjects)} rows")

# ═══════════════════════════════════════════════════════
# 6. CLASS SUBJECTS
# ═══════════════════════════════════════════════════════
class_subjects = []
used_combos = set()
for i in range(8):
    room = classrooms[i % len(classrooms)].class_code
    subj = subjects[(i * 2) % len(subjects)].subject_code
    while (sessions[-1].session_code, room, subj) in used_combos:
        room = classrooms[hash(str(i) + room) % len(classrooms)].class_code
        subj = subjects[hash(subj) % len(subjects)].subject_code
    used_combos.add((sessions[-1].session_code, room, subj))
    cs = ClassSubject(
        class_subject_code=generate_class_subject_code(),
        academic_sessions_id=sessions[-1].session_code,
        classroom_id=room,
        subject_id=subj,
        created_by=users[0].user_code,
    )
    session.add(cs)
    class_subjects.append(cs)
flush()
created["class_subjects"] = class_subjects
print(f"✓ class_subjects: {len(class_subjects)} rows")

# ═══════════════════════════════════════════════════════
# 7. TEACHER SUBJECTS
# ═══════════════════════════════════════════════════════
teacher_subjects = []
used_ts_combos = set()
for i, t in enumerate(teachers):
    ts_room = classrooms[i % len(classrooms)].class_code
    ts_subj = subjects[(i + 1) % len(subjects)].subject_code
    while (sessions[-1].session_code, ts_room, ts_subj) in used_ts_combos:
        ts_room = classrooms[hash(f"ts{i}") % len(classrooms)].class_code
        ts_subj = subjects[hash(f"ts_subj{i}") % len(subjects)].subject_code
    used_ts_combos.add((sessions[-1].session_code, ts_room, ts_subj))
    ts = TeacherSubject(
        teacher_subject_code=generate_teacher_subject_code(),
        academic_sessions_id=sessions[-1].session_code,
        class_subject_id=class_subjects[i % len(class_subjects)].class_subject_code,
        classroom_id=ts_room,
        subject_id=ts_subj,
        teacher_id=t.teacher_id,
    )
    session.add(ts)
    teacher_subjects.append(ts)
flush()
created["teacher_subjects"] = teacher_subjects
print(f"✓ teacher_subjects: {len(teacher_subjects)} rows")

# ═══════════════════════════════════════════════════════
# 8. STUDENT CLASSES
# ═══════════════════════════════════════════════════════
student_classes = []
for i, s in enumerate(students):
    sc = StudentClass(
        student_class_code=generate_student_class_code(),
        academic_sessions_id=sessions[-1].session_code,
        student_id=s.student_id,
        classroom_id=classrooms[i % len(classrooms)].class_code,
        roll_number=i + 1,
        admission_date=date(2026, 4, 1),
    )
    session.add(sc)
    student_classes.append(sc)
flush()
created["student_classes"] = student_classes
print(f"✓ student_classes: {len(student_classes)} rows")

# ═══════════════════════════════════════════════════════
# 9. WEEK DAYS
# ═══════════════════════════════════════════════════════
week_days = []
for i, (code, name) in enumerate([("MON", "Monday"), ("TUE", "Tuesday"), ("WED", "Wednesday"),
                                    ("THU", "Thursday"), ("FRI", "Friday")], 1):
    wd = WeekDay(day_code=code, day_name=name, display_order=i)
    session.add(wd)
    week_days.append(wd)
flush()
created["week_days"] = week_days
print(f"✓ week_days: {len(week_days)} rows")

# ═══════════════════════════════════════════════════════
# 10. TIME SLOTS
# ═══════════════════════════════════════════════════════
time_slots = []
slots_data = [
    ("P1", "First Period", time(8, 0), time(9, 0), 60, 1),
    ("P2", "Second Period", time(9, 0), time(10, 0), 60, 2),
    ("P3", "Third Period", time(10, 15), time(11, 15), 60, 3),
    ("P4", "Fourth Period", time(11, 15), time(12, 15), 60, 4),
]
for code, name, st, et, dur, order in slots_data:
    ts = TimeSlot(slot_code=code, slot_name=name, start_time=st, end_time=et,
                  duration_minutes=dur, display_order=order)
    session.add(ts)
    time_slots.append(ts)
flush()
created["time_slots"] = time_slots
print(f"✓ time_slots: {len(time_slots)} rows")

# ═══════════════════════════════════════════════════════
# 11. CLASS TIMETABLE
# ═══════════════════════════════════════════════════════
timetables = []
for i in range(8):
    tt = ClassTimeTable(
        timetable_code=generate_timetable_code(),
        academic_sessions_id=sessions[-1].session_code,
        classroom_id=classrooms[i % len(classrooms)].class_code,
        class_subject_id=class_subjects[i % len(class_subjects)].class_subject_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
        week_day_id=week_days[i % len(week_days)].day_code,
        time_slot_id=time_slots[i % len(time_slots)].slot_code,
    )
    session.add(tt)
    timetables.append(tt)
flush()
created["timetables"] = timetables
print(f"✓ class_timetable: {len(timetables)} rows")

# ═══════════════════════════════════════════════════════
# 12. TEACHER AVAILABILITY
# ═══════════════════════════════════════════════════════
availabilities = []
for i in range(5):
    av = TeacherAvailability(
        availability_code=generate_availability_code(),
        academic_sessions_id=sessions[-1].session_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
        week_day_id=week_days[i % len(week_days)].day_code,
        time_slot_id=time_slots[i % len(time_slots)].slot_code,
        is_available=True,
    )
    session.add(av)
    availabilities.append(av)
flush()
created["availabilities"] = availabilities
print(f"✓ teacher_availability: {len(availabilities)} rows")

# ═══════════════════════════════════════════════════════
# 13. FEES
# ═══════════════════════════════════════════════════════
fees = []
for i in range(8):
    f = Fee(
        fee_code=generate_fee_code(),
        academic_sessions_id=sessions[-1].session_code,
        student_class_id=student_classes[i % len(student_classes)].student_class_code,
        fee_month=(i % 12) + 1,
        fee_year=2026,
        total_amount=5000,
        paid_amount=5000 if i % 2 == 0 else 0,
        discount_amount=500 if i % 3 == 0 else 0,
        fine_amount=0,
        due_date=date(2026, (i % 12) + 1, 15),
        status=FeeStatus.PAID if i % 2 == 0 else FeeStatus.PENDING,
        created_by=users[0].user_code,
    )
    session.add(f)
    fees.append(f)
flush()
created["fees"] = fees
print(f"✓ fees: {len(fees)} rows")

# ═══════════════════════════════════════════════════════
# 14. NOTICES
# ═══════════════════════════════════════════════════════
notices = []
for i in range(6):
    n = Notice(
        notice_code=generate_notice_code(),
        academic_sessions_id=sessions[-1].session_code,
        title=f"Notice #{i+1}: General Announcement",
        description=f"Description for notice {i+1}",
        notice_type=NoticeType.GENERAL,
        audience=NoticeAudience.ALL,
        publish_date=date(2026, 7, 1 + i),
        created_by=users[0].user_code,
    )
    session.add(n)
    notices.append(n)
flush()
created["notices"] = notices
print(f"✓ notices: {len(notices)} rows")

# ═══════════════════════════════════════════════════════
# 15. ASSIGNMENTS
# ═══════════════════════════════════════════════════════
assignments = []
for i in range(6):
    a = Assignment(
        assignment_code=generate_assignment_code(),
        academic_sessions_id=sessions[-1].session_code,
        classroom_id=classrooms[i % len(classrooms)].class_code,
        class_subject_id=class_subjects[i % len(class_subjects)].class_subject_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
        title=f"Assignment {i+1}",
        due_date=date(2026, 8, 1 + i),
        total_marks=100,
        passing_marks=40,
        status=AssignmentStatus.PUBLISHED,
        created_by=users[0].user_code,
    )
    session.add(a)
    assignments.append(a)
flush()
created["assignments"] = assignments
print(f"✓ assignments: {len(assignments)} rows")

# ═══════════════════════════════════════════════════════
# 16. ASSIGNMENT RESULTS
# ═══════════════════════════════════════════════════════
assignment_results = []
for i in range(6):
    ar = AssignmentResult(
        assignment_result_code=generate_assignment_result_code(),
        assignment_id=assignments[i % len(assignments)].assignment_code,
        student_class_id=student_classes[i % len(student_classes)].student_class_code,
        obtained_marks=75 + i * 3,
        is_checked=True,
    )
    session.add(ar)
    assignment_results.append(ar)
flush()
created["assignment_results"] = assignment_results
print(f"✓ assignment_results: {len(assignment_results)} rows")

# ═══════════════════════════════════════════════════════
# 17. EXAMS
# ═══════════════════════════════════════════════════════
exams = []
for i in range(6):
    e = Exam(
        exam_code=generate_exam_code(),
        academic_sessions_id=sessions[-1].session_code,
        classroom_id=classrooms[i % len(classrooms)].class_code,
        class_subject_id=class_subjects[i % len(class_subjects)].class_subject_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
        exam_name=f"Term {i+1} Exam",
        exam_type="Midterm" if i % 2 == 0 else "Final",
        exam_date=date(2026, 9, 1 + i),
        total_marks=100,
        passing_marks=40,
        status=ExamStatus.PUBLISHED,
        created_by=users[0].user_code,
    )
    session.add(e)
    exams.append(e)
flush()
created["exams"] = exams
print(f"✓ exams: {len(exams)} rows")

# ═══════════════════════════════════════════════════════
# 18. EXAM RESULTS
# ═══════════════════════════════════════════════════════
exam_results = []
for i in range(6):
    er = ExamResult(
        exam_result_code=generate_exam_result_code(),
        exam_id=exams[i % len(exams)].exam_code,
        student_class_id=student_classes[i % len(student_classes)].student_class_code,
        obtained_marks=80 + i * 2,
        rank_in_class=i + 1,
    )
    session.add(er)
    exam_results.append(er)
flush()
created["exam_results"] = exam_results
print(f"✓ exam_results: {len(exam_results)} rows")

# ═══════════════════════════════════════════════════════
# 19. STUDY MATERIALS
# ═══════════════════════════════════════════════════════
materials = []
for i in range(5):
    m = StudyMaterial(
        material_code=generate_material_code(),
        academic_sessions_id=sessions[-1].session_code,
        classroom_id=classrooms[i % len(classrooms)].class_code,
        class_subject_id=class_subjects[i % len(class_subjects)].class_subject_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
        title=f"Material {i+1}",
        material_type=MaterialType.PDF,
        file_name=f"doc{i+1}.pdf",
        file_url=f"/uploads/study_materials/doc{i+1}.pdf",
        file_size=1024 * (i + 1),
        uploaded_by=users[0].user_code,
    )
    session.add(m)
    materials.append(m)
flush()
created["materials"] = materials
print(f"✓ study_materials: {len(materials)} rows")

# ═══════════════════════════════════════════════════════
# 20. CHAT ROOMS
# ═══════════════════════════════════════════════════════
chat_rooms = []
for i in range(5):
    cr = ChatRoom(
        chat_room_code=generate_chat_room_code(),
        academic_sessions_id=sessions[-1].session_code,
        student_class_id=student_classes[i % len(student_classes)].student_class_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
    )
    session.add(cr)
    chat_rooms.append(cr)
flush()
created["chat_rooms"] = chat_rooms
print(f"✓ chat_rooms: {len(chat_rooms)} rows")

# ═══════════════════════════════════════════════════════
# 21. CHAT MESSAGES
# ═══════════════════════════════════════════════════════
chat_messages = []
for i in range(8):
    cm = ChatMessage(
        chat_message_code=generate_chat_message_code(),
        chat_room_id=chat_rooms[i % len(chat_rooms)].chat_room_code,
        sender_id=users[i % len(users)].user_code,
        message=f"Hello from user {i+1}",
    )
    session.add(cm)
    chat_messages.append(cm)
flush()
created["chat_messages"] = chat_messages
print(f"✓ chat_messages: {len(chat_messages)} rows")

# ═══════════════════════════════════════════════════════
# 22. DAILY CLASSES
# ═══════════════════════════════════════════════════════
daily_classes = []
for i in range(6):
    dc = DailyClass(
        daily_class_code=generate_daily_class_code(),
        academic_sessions_id=sessions[-1].session_code,
        classroom_id=classrooms[i % len(classrooms)].class_code,
        class_subject_id=class_subjects[i % len(class_subjects)].class_subject_code,
        teacher_subject_id=teacher_subjects[i % len(teacher_subjects)].teacher_subject_code,
        timetable_id=timetables[i % len(timetables)].timetable_code,
        class_date=date(2026, 7, 22 + i),
        topic=f"Topic {i+1}",
        lecture_status="Completed",
    )
    session.add(dc)
    daily_classes.append(dc)
flush()
created["daily_classes"] = daily_classes
print(f"✓ daily_classes: {len(daily_classes)} rows")

# ═══════════════════════════════════════════════════════
# 23. DAILY CLASS STUDENTS
# ═══════════════════════════════════════════════════════
daily_class_students = []
for i in range(6):
    dcs = DailyClassStudent(
        daily_class_student_code=generate_daily_class_student_code(),
        daily_class_id=daily_classes[i % len(daily_classes)].daily_class_code,
        student_class_id=student_classes[i % len(student_classes)].student_class_code,
        attendance_status="Present",
        marked_by=users[0].user_code,
    )
    session.add(dcs)
    daily_class_students.append(dcs)
flush()
created["daily_class_students"] = daily_class_students
print(f"✓ daily_class_students: {len(daily_class_students)} rows")

# ═══════════════════════════════════════════════════════
# 24. STUDENT ATTENDANCE
# ═══════════════════════════════════════════════════════
attendances = []
for i, sc in enumerate(student_classes):
    sa = StudentAttendance(
        attendance_code=generate_attendance_code(),
        student_class_id=sc.student_class_code,
        total_classes=30,
        present_classes=25 - i,
        absent_classes=5 + i,
        attendance_percentage=(25 - i) / 30 * 100,
    )
    session.add(sa)
    attendances.append(sa)
flush()
created["attendances"] = attendances
print(f"✓ student_attendance: {len(attendances)} rows")

# ═══════════════════════════════════════════════════════
# 25. STUDENT PROMOTION HISTORY
# ═══════════════════════════════════════════════════════
promotions = []
for i in range(5):
    ph = StudentPromotionHistory(
        promotion_code=generate_promotion_code(),
        student_id=students[i % len(students)].student_id,
        from_session_id=sessions[0].session_code,
        to_session_id=sessions[1].session_code,
        from_classroom_id=classrooms[0].class_code,
        to_classroom_id=classrooms[1].class_code,
        previous_roll_number=i + 1,
        new_roll_number=i + 1,
        promotion_date=date(2024, 4, 1),
        promoted_by_user_id=users[0].user_code,
    )
    session.add(ph)
    promotions.append(ph)
flush()
created["promotions"] = promotions
print(f"✓ student_promotion_history: {len(promotions)} rows")

# ═══════════════════════════════════════════════════════
# 26. STUDENT ID CARDS
# ═══════════════════════════════════════════════════════
id_cards = []
for i, s in enumerate(students):
    ic = StudentIDCard(
        id_card_code=generate_id_card_code(),
        student_id=s.student_id,
        academic_sessions_id=sessions[-1].session_code,
        student_name=s.student_name,
        parent_name=f"Parent of {s.student_name}",
        class_display_name=classrooms[i % len(classrooms)].display_name,
        institute_name="Test School",
        institute_contact_number="1234567890",
        date_of_joining=date(2026, 4, 1),
        student_id_business=student_classes[i].student_class_code,
    )
    session.add(ic)
    id_cards.append(ic)
flush()
created["id_cards"] = id_cards
print(f"✓ student_id_cards: {len(id_cards)} rows")

# ═══════════════════════════════════════════════════════
# 27. ATTACHMENTS
# ═══════════════════════════════════════════════════════
attachments = []
for i in range(5):
    a = Attachment(
        attachment_code=generate_attachment_code(),
        entity_type="assignment",
        entity_id=assignments[i % len(assignments)].assignment_code,
        file_name=f"file{i+1}.pdf",
        mime_type="application/pdf",
        file_size=2048,
        file_data=b"dummy binary content",
        created_by=users[0].user_code,
    )
    session.add(a)
    attachments.append(a)
flush()
created["attachments"] = attachments
print(f"✓ attachments: {len(attachments)} rows")

# ═══════════════════════════════════════════════════════
# 28-30. KA COURSE / STUDENT / TOPIC
# ═══════════════════════════════════════════════════════
ka_courses = []
for i in range(5):
    kc = KaCourse(ka_course_code=generate_ka_course_code(), course_name=f"KA Course {i+1}", course_id=f"kc{i+1:03d}")
    session.add(kc)
    ka_courses.append(kc)
flush()
created["ka_courses"] = ka_courses

ka_students = []
for i in range(5):
    ks = KaStudent(ka_student_code=generate_ka_student_code(), student_name=f"KA Student {i+1}", email=f"ka{i+1}@test.com")
    session.add(ks)
    ka_students.append(ks)
flush()
created["ka_students"] = ka_students

topics = []
for i in range(6):
    t = Topic(topic_code=generate_topic_code(), course_id=ka_courses[i % len(ka_courses)].ka_course_code,
              topic_id=f"tid{i+1:03d}", topic_name=f"KA Topic {i+1}")
    session.add(t)
    topics.append(t)
flush()
created["topics"] = topics
print(f"✓ ka_tables: {len(ka_courses)} courses, {len(ka_students)} students, {len(topics)} topics")

# ═══════════════════════════════════════════════════════
# 31. KA TOPIC PROGRESS
# ═══════════════════════════════════════════════════════
topic_progress = []
for i in range(6):
    tp = TopicProgress(
        topic_progress_code=generate_topic_progress_code(),
        student_id=ka_students[i % len(ka_students)].ka_student_code,
        course_id=ka_courses[i % len(ka_courses)].ka_course_code,
        topic_id=topics[i % len(topics)].topic_code,
        point_available=100,
        point_earned=80 - i * 5,
        date=date(2026, 7, 1 + i),
    )
    session.add(tp)
    topic_progress.append(tp)
flush()
created["topic_progress"] = topic_progress
print(f"✓ ka_topic_progress: {len(topic_progress)} rows")

# ═══════════════════════════════════════════════════════
# 32. STUDENT REPORT
# ═══════════════════════════════════════════════════════
reports = []
for i in range(5):
    sr = StudentReport(report_code=generate_report_code(), student_id=ka_students[i % len(ka_students)].ka_student_code,
                       report_type="Monthly", created_at=datetime(2026, 7, 1 + i))
    session.add(sr)
    reports.append(sr)
flush()
created["reports"] = reports
print(f"✓ student_report: {len(reports)} rows")

# ═══════════════════════════════════════════════════════
# 33. STUDENT TOPIC PROGRESS REPORT
# ═══════════════════════════════════════════════════════
progress_reports = []
for i in range(5):
    spr = StudentTopicProgressReport(
        topic_progress_report_code=generate_topic_progress_report_code(),
        report_id=reports[i % len(reports)].report_code,
        topic_id=topics[i % len(topics)].topic_code,
        topic_progress_id=topic_progress[i % len(topic_progress)].topic_progress_code,
    )
    session.add(spr)
    progress_reports.append(spr)
flush()
created["progress_reports"] = progress_reports
print(f"✓ student_topic_progress_report: {len(progress_reports)} rows")

# ═══════════════════════════════════════════════════════
# 34-37. ZOOM TABLES
# ═══════════════════════════════════════════════════════
zoom_meetings = []
for i in range(5):
    zm = ZoomMeeting(uuid=f"zm-uuid-{i+1:03d}", meeting_id=1000 + i, topic=f"Meeting {i+1}",
                     start_time=datetime(2026, 7, 22 + i, 10, 0), duration=60)
    session.add(zm)
    zoom_meetings.append(zm)
flush()

zoom_files = []
for i in range(5):
    zf = ZoomFile(zoom_file_code=generate_zoom_file_code(), file_initial=f"FI{i+1:03d}",
                  raw_date="2026-07-22", raw_time="10:00", date="2026-07-22", time="10:00")
    session.add(zf)
    zoom_files.append(zf)
flush()

zoom_recordings = []
for i in range(5):
    zr = ZoomRecordingFile(id=f"rec-{i+1:03d}", meeting_uuid=zoom_meetings[i].uuid,
                           recording_start=datetime(2026, 7, 22 + i, 10, 0))
    session.add(zr)
    zoom_recordings.append(zr)
flush()
created["zoom_recordings"] = zoom_recordings

zoom_transcripts = []
for i in range(5):
    zt = ZoomTranscript(zoom_transcript_code=generate_zoom_transcript_code(),
                        zoom_file_id=zoom_recordings[i].id, sequence_index=i,
                        start_time="00:00", end_time="01:00", duration=60.0,
                        speaker=f"Speaker {i+1}", text=f"Transcript text {i+1}")
    session.add(zt)
    zoom_transcripts.append(zt)
flush()

zoom_interactions = []
for i in range(5):
    zi = ZoomStudentInteraction(zoom_interaction_code=generate_zoom_interaction_code(),
                                zoom_file_id=zoom_recordings[i].id,
                                interaction_time="00:30", interaction_duration=5.0,
                                speaker_name=f"Student {i+1}")
    session.add(zi)
    zoom_interactions.append(zi)
flush()

duration_reports = []
for i in range(5):
    dr = ZoomDurationReport(duration_report_code=generate_duration_report_code(),
                            report_id=reports[i % len(reports)].report_code,
                            mean_duration_minutes=30, min_duration_minutes=10, max_duration_minutes=60)
    session.add(dr)
    duration_reports.append(dr)
flush()

interaction_reports = []
for i in range(5):
    ir = ZoomInteractionReport(interaction_report_code=generate_interaction_report_code(),
                                report_id=reports[i % len(reports)].report_code,
                                mean_interaction_count=5, min_interaction_count=1, max_interaction_count=10)
    session.add(ir)
    interaction_reports.append(ir)
flush()
print(f"✓ zoom tables: all seeded")

# ═══════════════════════════════════════════════════════
# VERIFY ALL ROWS
# ═══════════════════════════════════════════════════════
session.commit()

inspector = inspect(engine)
all_tables = inspector.get_table_names()
print("\n" + "=" * 60)
print("FINAL VERIFICATION - All tables with row counts:")
print("=" * 60)
total = 0
for table in sorted(all_tables):
    count = session.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
    print(f"  {table:45s} {count:3d} rows")
    total += count
print("-" * 60)
print(f"  {'TOTAL':45s} {total:3d} rows")
print("=" * 60)
print("\n✅ DATA SEEDING COMPLETE!")
session.close()
