"""v3_convert_all_ids_to_business_ids

Revision ID: a1b2c3d4e5f6
Revises: 183909ac2803
Create Date: 2026-07-20 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "183909ac2803"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ============================================================
    # STEP 1: Drop ALL FK constraints referencing users.id
    # ============================================================
    op.drop_constraint(
        "student_profiles_user_id_fkey", "student_profiles", type_="foreignkey"
    )
    op.drop_constraint(
        "teacher_profiles_user_id_fkey", "teacher_profiles", type_="foreignkey"
    )
    op.drop_constraint(
        "admin_profiles_user_id_fkey", "admin_profiles", type_="foreignkey"
    )
    op.drop_constraint("assignments_created_by_fkey", "assignments", type_="foreignkey")
    op.drop_constraint("assignments_updated_by_fkey", "assignments", type_="foreignkey")
    op.drop_constraint("assignments_deleted_by_fkey", "assignments", type_="foreignkey")
    op.drop_constraint(
        "assignments_uploaded_by_fkey", "assignments", type_="foreignkey"
    )
    op.drop_constraint(
        "assignment_results_checked_by_fkey", "assignment_results", type_="foreignkey"
    )
    op.drop_constraint("exams_created_by_fkey", "exams", type_="foreignkey")
    op.drop_constraint("exams_updated_by_fkey", "exams", type_="foreignkey")
    op.drop_constraint("exams_deleted_by_fkey", "exams", type_="foreignkey")
    op.drop_constraint(
        "exam_results_checked_by_fkey", "exam_results", type_="foreignkey"
    )
    op.drop_constraint("fees_created_by_fkey", "fees", type_="foreignkey")
    op.drop_constraint("fees_updated_by_fkey", "fees", type_="foreignkey")
    op.drop_constraint("fees_deleted_by_fkey", "fees", type_="foreignkey")
    op.drop_constraint("notices_created_by_fkey", "notices", type_="foreignkey")
    op.drop_constraint("notices_updated_by_fkey", "notices", type_="foreignkey")
    op.drop_constraint("notices_deleted_by_fkey", "notices", type_="foreignkey")
    op.drop_constraint(
        "study_materials_uploaded_by_fkey", "study_materials", type_="foreignkey"
    )
    op.drop_constraint(
        "chat_messages_sender_id_fkey", "chat_messages", type_="foreignkey"
    )
    op.drop_constraint(
        "daily_class_students_marked_by_fkey",
        "daily_class_students",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_promotion_history_promoted_by_user_id_fkey",
        "student_promotion_history",
        type_="foreignkey",
    )
    op.drop_constraint("classroom_created_by_fkey", "classroom", type_="foreignkey")
    op.drop_constraint("classroom_updated_by_fkey", "classroom", type_="foreignkey")
    op.drop_constraint("subjects_created_by_fkey", "subjects", type_="foreignkey")
    op.drop_constraint("subjects_updated_by_fkey", "subjects", type_="foreignkey")
    op.drop_constraint(
        "class_subjects_created_by_fkey", "class_subjects", type_="foreignkey"
    )
    op.drop_constraint(
        "class_subjects_updated_by_fkey", "class_subjects", type_="foreignkey"
    )

    # ============================================================
    # STEP 2: Drop FK constraints referencing other tables' old .id
    # ============================================================
    # assignments -> old tables
    op.drop_constraint(
        "assignments_class_subject_id_fkey", "assignments", type_="foreignkey"
    )
    op.drop_constraint(
        "assignments_teacher_subject_id_fkey", "assignments", type_="foreignkey"
    )
    # assignment_results
    op.drop_constraint(
        "assignment_results_assignment_id_fkey",
        "assignment_results",
        type_="foreignkey",
    )
    op.drop_constraint(
        "assignment_results_student_class_id_fkey",
        "assignment_results",
        type_="foreignkey",
    )
    # exams
    op.drop_constraint("exams_class_subject_id_fkey", "exams", type_="foreignkey")
    op.drop_constraint("exams_teacher_subject_id_fkey", "exams", type_="foreignkey")
    # exam_results
    op.drop_constraint("exam_results_exam_id_fkey", "exam_results", type_="foreignkey")
    op.drop_constraint(
        "exam_results_student_class_id_fkey", "exam_results", type_="foreignkey"
    )
    # fees
    op.drop_constraint("fees_student_class_id_fkey", "fees", type_="foreignkey")
    # study_materials
    op.drop_constraint(
        "study_materials_class_subject_id_fkey", "study_materials", type_="foreignkey"
    )
    op.drop_constraint(
        "study_materials_teacher_subject_id_fkey", "study_materials", type_="foreignkey"
    )
    # chat
    op.drop_constraint(
        "chat_rooms_student_class_id_fkey", "chat_rooms", type_="foreignkey"
    )
    op.drop_constraint(
        "chat_rooms_teacher_subject_id_fkey", "chat_rooms", type_="foreignkey"
    )
    op.drop_constraint(
        "chat_messages_chat_room_id_fkey", "chat_messages", type_="foreignkey"
    )
    # daily_class
    op.drop_constraint(
        "daily_classes_class_subject_id_fkey", "daily_classes", type_="foreignkey"
    )
    op.drop_constraint(
        "daily_classes_teacher_subject_id_fkey", "daily_classes", type_="foreignkey"
    )
    op.drop_constraint(
        "daily_classes_timetable_id_fkey", "daily_classes", type_="foreignkey"
    )
    op.drop_constraint(
        "daily_class_students_daily_class_id_fkey",
        "daily_class_students",
        type_="foreignkey",
    )
    op.drop_constraint(
        "daily_class_students_student_class_id_fkey",
        "daily_class_students",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_attendance_student_class_id_fkey",
        "student_attendance",
        type_="foreignkey",
    )
    # timetable
    op.drop_constraint(
        "class_timetable_class_subject_id_fkey", "class_timetable", type_="foreignkey"
    )
    op.drop_constraint(
        "class_timetable_teacher_subject_id_fkey", "class_timetable", type_="foreignkey"
    )
    # teacher_subjects
    op.drop_constraint(
        "teacher_subjects_class_subject_id_fkey", "teacher_subjects", type_="foreignkey"
    )
    # zoom
    op.drop_constraint(
        "zoom_duration_report_report_id_fkey",
        "zoom_duration_report",
        type_="foreignkey",
    )
    op.drop_constraint(
        "zoom_interaction_report_report_id_fkey",
        "zoom_interaction_report",
        type_="foreignkey",
    )
    # topic
    op.drop_constraint("ka_topic_course_id_fkey", "ka_topic", type_="foreignkey")
    op.drop_constraint(
        "ka_topic_progress_student_id_fkey", "ka_topic_progress", type_="foreignkey"
    )
    op.drop_constraint(
        "ka_topic_progress_course_id_fkey", "ka_topic_progress", type_="foreignkey"
    )
    op.drop_constraint(
        "ka_topic_progress_topic_id_fkey", "ka_topic_progress", type_="foreignkey"
    )
    op.drop_constraint(
        "student_topic_progress_report_report_id_fkey",
        "student_topic_progress_report",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_topic_progress_report_topic_id_fkey",
        "student_topic_progress_report",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_topic_progress_report_topic_progress_id_fkey",
        "student_topic_progress_report",
        type_="foreignkey",
    )

    # ============================================================
    # STEP 2b: Drop FK constraints referencing users.teacher_id,
    #          users.student_id, users.admin_id (these depend on
    #          the unique indexes we are about to drop)
    # ============================================================
    op.drop_constraint(
        "teacher_profiles_teacher_id_fkey", "teacher_profiles", type_="foreignkey"
    )
    op.drop_constraint(
        "student_profiles_student_id_fkey", "student_profiles", type_="foreignkey"
    )

    # ============================================================
    # STEP 3: Drop unique indexes on business_id columns (will become PKs)
    # ============================================================
    op.drop_index("ix_users_admin_id", table_name="users")
    op.drop_index("ix_users_teacher_id", table_name="users")
    op.drop_index("ix_users_student_id", table_name="users")
    op.drop_index("ix_assignments_assignment_id", table_name="assignments")
    op.drop_index("ix_exams_exam_id", table_name="exams")
    op.drop_index("ix_fees_fee_id", table_name="fees")
    op.drop_index("ix_notices_notice_id", table_name="notices")
    op.drop_index("ix_study_materials_material_id", table_name="study_materials")
    op.drop_index("ix_chat_rooms_chat_room_id", table_name="chat_rooms")
    op.drop_index("ix_class_timetable_timetable_id", table_name="class_timetable")
    op.drop_index(
        "ix_teacher_availability_availability_id", table_name="teacher_availability"
    )
    op.drop_index("ix_attachments_attachment_code", table_name="attachments")

    # ============================================================
    # STEP 4: Drop unique constraints on business_id columns
    # ============================================================
    op.drop_constraint("assignments_assignment_id_key", "assignments", type_="unique")
    op.drop_constraint("exams_exam_id_key", "exams", type_="unique")
    op.drop_constraint("fees_fee_id_key", "fees", type_="unique")
    op.drop_constraint("notices_notice_id_key", "notices", type_="unique")
    op.drop_constraint(
        "study_materials_material_id_key", "study_materials", type_="unique"
    )
    op.drop_constraint("chat_rooms_chat_room_id_key", "chat_rooms", type_="unique")
    op.drop_constraint(
        "class_timetable_timetable_id_key", "class_timetable", type_="unique"
    )
    op.drop_constraint(
        "teacher_availability_availability_id_key",
        "teacher_availability",
        type_="unique",
    )
    op.drop_constraint("attachments_attachment_code_key", "attachments", type_="unique")

    # ============================================================
    # STEP 5: Drop old id columns from parent tables
    # ============================================================
    op.drop_column("users", "id")
    op.drop_column("assignments", "id")
    op.drop_column("assignment_results", "id")
    op.drop_column("exams", "id")
    op.drop_column("exam_results", "id")
    op.drop_column("fees", "id")
    op.drop_column("notices", "id")
    op.drop_column("study_materials", "id")
    op.drop_column("chat_rooms", "id")
    op.drop_column("chat_messages", "id")
    op.drop_column("class_subjects", "id")
    op.drop_column("class_timetable", "id")
    op.drop_column("teacher_availability", "id")
    op.drop_column("daily_classes", "id")
    op.drop_column("daily_class_students", "id")
    op.drop_column("student_attendance", "id")
    op.drop_column("teacher_subjects", "id")
    op.drop_column("student_classes", "id")
    op.drop_column("student_promotion_history", "id")
    op.drop_column("student_id_cards", "id")
    op.drop_column("student_report", "id")
    op.drop_column("attachments", "id")
    op.drop_column("ka_course", "id")
    op.drop_column("ka_student", "id")
    op.drop_column("ka_topic", "id")
    op.drop_column("ka_topic_progress", "id")
    op.drop_column("student_topic_progress_report", "id")
    op.drop_column("zoom_file", "id")
    op.drop_column("zoom_transcript", "id")
    op.drop_column("zoom_student_interaction", "id")
    op.drop_column("zoom_duration_report", "id")
    op.drop_column("zoom_interaction_report", "id")

    # ============================================================
    # STEP 5b: Remove old business_id columns that are being
    #           replaced (the ones that had separate id + business_id)
    # ============================================================
    op.drop_column("assignments", "assignment_id")
    op.drop_column("exams", "exam_id")
    op.drop_column("fees", "fee_id")
    op.drop_column("notices", "notice_id")
    op.drop_column("study_materials", "material_id")
    op.drop_column("chat_rooms", "chat_room_id")
    op.drop_column("class_timetable", "timetable_id")
    op.drop_column("teacher_availability", "availability_id")
    op.drop_column("daily_classes", "daily_class_id")
    op.drop_column("attachments", "attachment_code")

    # ============================================================
    # STEP 6: Rename remaining business_id-like columns -> business_id
    #         for tables that already had string PKs with different names
    # ============================================================
    # users: admin_id, teacher_id, student_id stay as-is
    # but we need to add business_id column
    op.add_column(
        "users", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_users", "users", ["business_id"])

    # Add business_id columns with PK for all other tables
    op.add_column(
        "assignments", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_assignments", "assignments", ["business_id"])

    op.add_column(
        "assignment_results",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_assignment_results", "assignment_results", ["business_id"]
    )

    op.add_column(
        "exams", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_exams", "exams", ["business_id"])

    op.add_column(
        "exam_results", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_exam_results", "exam_results", ["business_id"])

    op.add_column(
        "fees", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_fees", "fees", ["business_id"])

    op.add_column(
        "notices", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_notices", "notices", ["business_id"])

    op.add_column(
        "study_materials",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_study_materials", "study_materials", ["business_id"])

    op.add_column(
        "chat_rooms", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_chat_rooms", "chat_rooms", ["business_id"])

    op.add_column(
        "chat_messages", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_chat_messages", "chat_messages", ["business_id"])

    op.add_column(
        "class_subjects", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_class_subjects", "class_subjects", ["business_id"])

    op.add_column(
        "class_timetable",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_class_timetable", "class_timetable", ["business_id"])

    op.add_column(
        "teacher_availability",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_teacher_availability", "teacher_availability", ["business_id"]
    )

    op.add_column(
        "daily_classes", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_daily_classes", "daily_classes", ["business_id"])

    op.add_column(
        "daily_class_students",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_daily_class_students", "daily_class_students", ["business_id"]
    )

    op.add_column(
        "student_attendance",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_student_attendance", "student_attendance", ["business_id"]
    )

    op.add_column(
        "teacher_subjects",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_teacher_subjects", "teacher_subjects", ["business_id"])

    op.add_column(
        "student_classes",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_student_classes", "student_classes", ["business_id"])

    op.add_column(
        "student_promotion_history",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_student_promotion_history", "student_promotion_history", ["business_id"]
    )

    op.add_column(
        "student_id_cards",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_student_id_cards", "student_id_cards", ["business_id"])

    op.add_column(
        "student_report", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_student_report", "student_report", ["business_id"])

    op.add_column(
        "attachments", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_attachments", "attachments", ["business_id"])

    op.add_column(
        "ka_course", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_ka_course", "ka_course", ["business_id"])

    op.add_column(
        "ka_student", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_ka_student", "ka_student", ["business_id"])

    op.add_column(
        "ka_topic", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_ka_topic", "ka_topic", ["business_id"])

    op.add_column(
        "ka_topic_progress",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_ka_topic_progress", "ka_topic_progress", ["business_id"])

    op.add_column(
        "student_topic_progress_report",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_student_topic_progress_report",
        "student_topic_progress_report",
        ["business_id"],
    )

    op.add_column(
        "zoom_file", sa.Column("business_id", sa.String(length=30), nullable=False)
    )
    op.create_primary_key("pk_zoom_file", "zoom_file", ["business_id"])

    op.add_column(
        "zoom_transcript",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key("pk_zoom_transcript", "zoom_transcript", ["business_id"])

    op.add_column(
        "zoom_student_interaction",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_zoom_student_interaction", "zoom_student_interaction", ["business_id"]
    )

    op.add_column(
        "zoom_duration_report",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_zoom_duration_report", "zoom_duration_report", ["business_id"]
    )

    op.add_column(
        "zoom_interaction_report",
        sa.Column("business_id", sa.String(length=30), nullable=False),
    )
    op.create_primary_key(
        "pk_zoom_interaction_report", "zoom_interaction_report", ["business_id"]
    )

    # ============================================================
    # STEP 7: Alter FK column types from INTEGER to String(30)
    # ============================================================
    # User references
    op.alter_column(
        "student_profiles",
        "user_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_profiles",
        "user_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "admin_profiles",
        "user_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "assignments",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "assignments",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "assignments",
        "deleted_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "assignments",
        "uploaded_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "exams",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "exams",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "exams",
        "deleted_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "fees",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "fees",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "fees",
        "deleted_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "notices",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "notices",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "notices",
        "deleted_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "study_materials",
        "uploaded_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "chat_messages",
        "sender_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_class_students",
        "marked_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "student_promotion_history",
        "promoted_by_user_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "assignment_results",
        "checked_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "exam_results",
        "checked_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "classroom",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "classroom",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "subjects",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "subjects",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "class_subjects",
        "created_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "class_subjects",
        "updated_by",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )

    # FK references between entity tables
    op.alter_column(
        "assignments",
        "class_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "assignments",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "assignment_results",
        "assignment_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "assignment_results",
        "student_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "exams",
        "class_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "exams",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "exam_results",
        "exam_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "exam_results",
        "student_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "fees",
        "student_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "study_materials",
        "class_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "study_materials",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "chat_rooms",
        "student_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "chat_rooms",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "chat_messages",
        "chat_room_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_classes",
        "class_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_classes",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_classes",
        "timetable_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "daily_class_students",
        "daily_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_class_students",
        "student_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_attendance",
        "student_class_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "class_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_subjects",
        "class_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_availability",
        "teacher_subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "attachments",
        "entity_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "zoom_duration_report",
        "report_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "zoom_interaction_report",
        "report_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "ka_topic",
        "course_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "ka_topic_progress",
        "student_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "ka_topic_progress",
        "course_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "ka_topic_progress",
        "topic_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        "student_topic_progress_report",
        "report_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_topic_progress_report",
        "topic_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_topic_progress_report",
        "topic_progress_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    # ============================================================
    # STEP 8: Recreate FK constraints pointing to business_id columns
    # ============================================================
    # Users FK
    op.create_foreign_key(
        "fk_student_profiles_user",
        "student_profiles",
        "users",
        ["user_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_teacher_profiles_user",
        "teacher_profiles",
        "users",
        ["user_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_admin_profiles_user",
        "admin_profiles",
        "users",
        ["user_id"],
        ["business_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_assignments_creator",
        "assignments",
        "users",
        ["created_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignments_updater",
        "assignments",
        "users",
        ["updated_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignments_deleter",
        "assignments",
        "users",
        ["deleted_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignments_uploader",
        "assignments",
        "users",
        ["uploaded_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignment_results_checker",
        "assignment_results",
        "users",
        ["checked_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_exams_creator", "exams", "users", ["created_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_exams_updater", "exams", "users", ["updated_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_exams_deleter", "exams", "users", ["deleted_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_exam_results_checker",
        "exam_results",
        "users",
        ["checked_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_fees_creator", "fees", "users", ["created_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_fees_updater", "fees", "users", ["updated_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_fees_deleter", "fees", "users", ["deleted_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_notices_creator", "notices", "users", ["created_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_notices_updater", "notices", "users", ["updated_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_notices_deleter", "notices", "users", ["deleted_by"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_study_materials_uploader",
        "study_materials",
        "users",
        ["uploaded_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_chat_messages_sender",
        "chat_messages",
        "users",
        ["sender_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_daily_class_students_marker",
        "daily_class_students",
        "users",
        ["marked_by"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_student_promotion_history_promoter",
        "student_promotion_history",
        "users",
        ["promoted_by_user_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_classroom_creator",
        "classroom",
        "users",
        ["created_by"],
        ["business_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_classroom_updater",
        "classroom",
        "users",
        ["updated_by"],
        ["business_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_subjects_creator",
        "subjects",
        "users",
        ["created_by"],
        ["business_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_subjects_updater",
        "subjects",
        "users",
        ["updated_by"],
        ["business_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_class_subjects_creator",
        "class_subjects",
        "users",
        ["created_by"],
        ["business_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_class_subjects_updater",
        "class_subjects",
        "users",
        ["updated_by"],
        ["business_id"],
        ondelete="SET NULL",
    )

    # FKs referencing users.teacher_id / users.student_id (recreated after dropping old ones in Step 2b)
    op.create_foreign_key(
        "fk_teacher_profiles_teacher_id",
        "teacher_profiles",
        "users",
        ["teacher_id"],
        ["teacher_id"],
    )
    op.create_foreign_key(
        "fk_student_profiles_student_id",
        "student_profiles",
        "users",
        ["student_id"],
        ["student_id"],
    )

    # Entity FK references
    op.create_foreign_key(
        "fk_assignments_class_subject",
        "assignments",
        "class_subjects",
        ["class_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignments_teacher_subject",
        "assignments",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignment_results_assignment",
        "assignment_results",
        "assignments",
        ["assignment_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_assignment_results_student_class",
        "assignment_results",
        "student_classes",
        ["student_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_exams_class_subject",
        "exams",
        "class_subjects",
        ["class_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_exams_teacher_subject",
        "exams",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_exam_results_exam", "exam_results", "exams", ["exam_id"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_exam_results_student_class",
        "exam_results",
        "student_classes",
        ["student_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_fees_student_class",
        "fees",
        "student_classes",
        ["student_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_study_materials_class_subject",
        "study_materials",
        "class_subjects",
        ["class_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_study_materials_teacher_subject",
        "study_materials",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_chat_rooms_student_class",
        "chat_rooms",
        "student_classes",
        ["student_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_chat_rooms_teacher_subject",
        "chat_rooms",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_chat_messages_room",
        "chat_messages",
        "chat_rooms",
        ["chat_room_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_daily_classes_class_subject",
        "daily_classes",
        "class_subjects",
        ["class_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_daily_classes_teacher_subject",
        "daily_classes",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_daily_classes_timetable",
        "daily_classes",
        "class_timetable",
        ["timetable_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_daily_class_students_daily_class",
        "daily_class_students",
        "daily_classes",
        ["daily_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_daily_class_students_student_class",
        "daily_class_students",
        "student_classes",
        ["student_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_student_attendance_student_class",
        "student_attendance",
        "student_classes",
        ["student_class_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_class_timetable_class_subject",
        "class_timetable",
        "class_subjects",
        ["class_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_class_timetable_teacher_subject",
        "class_timetable",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_teacher_subjects_class_subject",
        "teacher_subjects",
        "class_subjects",
        ["class_subject_id"],
        ["business_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_teacher_availability_teacher_subject",
        "teacher_availability",
        "teacher_subjects",
        ["teacher_subject_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_zoom_duration_report_student_report",
        "zoom_duration_report",
        "student_report",
        ["report_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_zoom_interaction_report_student_report",
        "zoom_interaction_report",
        "student_report",
        ["report_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_ka_topic_course", "ka_topic", "ka_course", ["course_id"], ["business_id"]
    )
    op.create_foreign_key(
        "fk_ka_topic_progress_student",
        "ka_topic_progress",
        "ka_student",
        ["student_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_ka_topic_progress_course",
        "ka_topic_progress",
        "ka_course",
        ["course_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_ka_topic_progress_topic",
        "ka_topic_progress",
        "ka_topic",
        ["topic_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_student_topic_progress_report_report",
        "student_topic_progress_report",
        "student_report",
        ["report_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_student_topic_progress_report_topic",
        "student_topic_progress_report",
        "ka_topic",
        ["topic_id"],
        ["business_id"],
    )
    op.create_foreign_key(
        "fk_student_topic_progress_report_progress",
        "student_topic_progress_report",
        "ka_topic_progress",
        ["topic_progress_id"],
        ["business_id"],
    )


def downgrade() -> None:
    """Revert all changes - restore integer PKs."""
    # This is a complex reverse migration.
    # In production, restore from backup instead.
