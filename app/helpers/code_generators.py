# app/helpers/code_generators.py

import secrets
import string
import uuid

from app.core.constants import (
    ADMIN_PREFIX,
    ASSIGNMENT_PREFIX,
    AVAILABILITY_PREFIX,
    CHAT_PREFIX,
    EXAM_PREFIX,
    FEE_PREFIX,
    MATERIAL_PREFIX,
    NOTICE_PREFIX,
    RECEIPT_PREFIX,
    REGISTRATION_PREFIX,
    STUDENT_PREFIX,
    TEACHER_PREFIX,
    TIMETABLE_PREFIX,
)


def generate_uuid():
    return str(uuid.uuid4())


def random_code(length: int = 6):
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_student_id(user_id: str | int = "") -> str:
    return f"{STUDENT_PREFIX}{random_code(8)}"


def generate_teacher_id(user_id: str | int = "") -> str:
    return f"{TEACHER_PREFIX}{random_code(8)}"


def generate_admin_id(user_id: str | int = "") -> str:
    return f"{ADMIN_PREFIX}{random_code(8)}"


# ------------------------------------------------------------
# No-arg generators for use as SQLAlchemy Column(default=...)
# (the row's own id/user_id isn't known yet at insert time,
# so these use a random suffix instead)
# ------------------------------------------------------------


def generate_admin_code() -> str:
    return f"{ADMIN_PREFIX}-{random_code(8)}"


def generate_assignment_id() -> str:
    return f"{ASSIGNMENT_PREFIX}-{random_code(8)}"


def generate_material_id() -> str:
    return f"{MATERIAL_PREFIX}-{random_code(8)}"


def generate_notice_code() -> str:
    return f"{NOTICE_PREFIX}-{random_code(8)}"


def generate_assignment_code() -> str:
    return f"{ASSIGNMENT_PREFIX}-{random_code(8)}"


def generate_exam_code() -> str:
    return f"{EXAM_PREFIX}-{random_code(8)}"


def generate_fee_code() -> str:
    return f"{FEE_PREFIX}-{random_code(8)}"


def generate_receipt_no() -> str:
    return f"{RECEIPT_PREFIX}-{random_code(10)}"


def generate_chat_room_id() -> str:
    return f"{CHAT_PREFIX}-{random_code(8)}"


def generate_timetable_id(academic_sessions_id: int, sequence: int) -> str:
    return f"{TIMETABLE_PREFIX}-{academic_sessions_id}-{sequence:06d}"


def generate_availability_id(academic_sessions_id: int, sequence: int) -> str:
    return f"{AVAILABILITY_PREFIX}-{academic_sessions_id}-{sequence:06d}"


def generate_session_name(start_year: int, end_year: int) -> str:
    return f"{start_year}-{str(end_year)[-2:]}"


def generate_subject_code(subject_name: str, class_name: str) -> str:
    words = subject_name.upper().split()
    prefix = words[0][:2] if len(words) == 1 else "".join(word[0] for word in words)[:2]
    digits = "".join(filter(str.isdigit, class_name))
    return f"{prefix}{digits}"


def generate_registration_number(year: int, sequence: int) -> str:
    """e.g. REG-2026-00001. `sequence` must be caller-computed (see
    RegistrationNumberService for the collision-safe generation loop) —
    this function only formats it.
    """
    return f"{REGISTRATION_PREFIX}-{year}-{sequence:05d}"


# ------------------------------------------------------------
# Business ID generators for models that currently lack a
# dedicated business-identifier function.
# ------------------------------------------------------------


def generate_user_business_id() -> str:
    return f"USR-{random_code(8)}"


def generate_assignment_result_id() -> str:
    return f"ASR-{random_code(8)}"


def generate_chat_message_id() -> str:
    return f"MSG-{random_code(8)}"


def generate_class_subject_id() -> str:
    return f"CLS-{random_code(8)}"


def generate_daily_class_student_id() -> str:
    return f"DCS-{random_code(8)}"


def generate_student_attendance_id() -> str:
    return f"ATT-{random_code(8)}"


def generate_exam_result_id() -> str:
    return f"EXR-{random_code(8)}"


def generate_teacher_subject_id() -> str:
    return f"TCH-{random_code(8)}"


def generate_student_class_id() -> str:
    return f"STC-{random_code(8)}"


def generate_promotion_history_id() -> str:
    return f"PRM-{random_code(8)}"


def generate_student_id_card_id() -> str:
    return f"IDC-{random_code(8)}"


def generate_student_report_id() -> str:
    return f"RPT-{random_code(8)}"


def generate_zoom_file_id() -> str:
    return f"ZFL-{random_code(8)}"


def generate_zoom_transcript_id() -> str:
    return f"ZTR-{random_code(8)}"


def generate_zoom_interaction_id() -> str:
    return f"ZIN-{random_code(8)}"


def generate_zoom_duration_report_id() -> str:
    return f"ZDR-{random_code(8)}"


def generate_zoom_interaction_report_id() -> str:
    return f"ZIR-{random_code(8)}"


def generate_ka_course_id() -> str:
    return f"KAC-{random_code(8)}"


def generate_ka_student_id() -> str:
    return f"KAS-{random_code(8)}"


def generate_topic_id() -> str:
    return f"TOP-{random_code(8)}"


def generate_topic_progress_id() -> str:
    return f"TPR-{random_code(8)}"
