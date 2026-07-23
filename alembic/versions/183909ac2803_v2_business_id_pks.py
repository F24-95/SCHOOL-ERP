"""v2_business_id_pks

Revision ID: 183909ac2803
Revises:
Create Date: 2026-07-20 18:22:56.364799

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "183909ac2803"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Step 1: Drop ALL FK constraints referencing parent table `id` columns first
    # (before dropping the id columns themselves)

    # FKs referencing academic_sessions.id
    op.drop_constraint(
        "assignments_academic_sessions_id_fkey", "assignments", type_="foreignkey"
    )
    op.drop_constraint(
        "chat_rooms_academic_sessions_id_fkey", "chat_rooms", type_="foreignkey"
    )
    op.drop_constraint(
        "class_subjects_academic_sessions_id_fkey", "class_subjects", type_="foreignkey"
    )
    op.drop_constraint(
        "class_timetable_academic_sessions_id_fkey",
        "class_timetable",
        type_="foreignkey",
    )
    op.drop_constraint(
        "classroom_academic_sessions_id_fkey", "classroom", type_="foreignkey"
    )
    op.drop_constraint(
        "daily_classes_academic_sessions_id_fkey", "daily_classes", type_="foreignkey"
    )
    op.drop_constraint("exams_academic_sessions_id_fkey", "exams", type_="foreignkey")
    op.drop_constraint("fees_academic_sessions_id_fkey", "fees", type_="foreignkey")
    op.drop_constraint(
        "notices_academic_sessions_id_fkey", "notices", type_="foreignkey"
    )
    op.drop_constraint(
        "student_classes_academic_sessions_id_fkey",
        "student_classes",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_id_cards_academic_sessions_id_fkey",
        "student_id_cards",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_promotion_history_from_session_id_fkey",
        "student_promotion_history",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_promotion_history_to_session_id_fkey",
        "student_promotion_history",
        type_="foreignkey",
    )
    op.drop_constraint(
        "study_materials_academic_sessions_id_fkey",
        "study_materials",
        type_="foreignkey",
    )
    op.drop_constraint(
        "teacher_availability_academic_sessions_id_fkey",
        "teacher_availability",
        type_="foreignkey",
    )
    op.drop_constraint(
        "teacher_subjects_academic_sessions_id_fkey",
        "teacher_subjects",
        type_="foreignkey",
    )

    # FKs referencing classroom.id
    op.drop_constraint(
        "assignments_classroom_id_fkey", "assignments", type_="foreignkey"
    )
    op.drop_constraint(
        "class_subjects_classroom_id_fkey", "class_subjects", type_="foreignkey"
    )
    op.drop_constraint(
        "class_timetable_classroom_id_fkey", "class_timetable", type_="foreignkey"
    )
    op.drop_constraint(
        "daily_classes_classroom_id_fkey", "daily_classes", type_="foreignkey"
    )
    op.drop_constraint("exams_classroom_id_fkey", "exams", type_="foreignkey")
    op.drop_constraint("notices_classroom_id_fkey", "notices", type_="foreignkey")
    op.drop_constraint(
        "student_classes_classroom_id_fkey", "student_classes", type_="foreignkey"
    )
    op.drop_constraint(
        "student_promotion_history_from_classroom_id_fkey",
        "student_promotion_history",
        type_="foreignkey",
    )
    op.drop_constraint(
        "student_promotion_history_to_classroom_id_fkey",
        "student_promotion_history",
        type_="foreignkey",
    )
    op.drop_constraint(
        "study_materials_classroom_id_fkey", "study_materials", type_="foreignkey"
    )
    op.drop_constraint(
        "teacher_subjects_classroom_id_fkey", "teacher_subjects", type_="foreignkey"
    )

    # FKs referencing subjects.id
    op.drop_constraint(
        "class_subjects_subject_id_fkey", "class_subjects", type_="foreignkey"
    )
    op.drop_constraint(
        "teacher_subjects_subject_id_fkey", "teacher_subjects", type_="foreignkey"
    )

    # FKs referencing time_slots.id
    op.drop_constraint(
        "class_timetable_time_slot_id_fkey", "class_timetable", type_="foreignkey"
    )
    op.drop_constraint(
        "teacher_availability_time_slot_id_fkey",
        "teacher_availability",
        type_="foreignkey",
    )

    # FKs referencing week_days.id
    op.drop_constraint(
        "class_timetable_week_day_id_fkey", "class_timetable", type_="foreignkey"
    )
    op.drop_constraint(
        "teacher_availability_week_day_id_fkey",
        "teacher_availability",
        type_="foreignkey",
    )

    # Step 2: Drop old unique indexes (they become PKs now)
    op.drop_index("ix_academic_sessions_session_code", table_name="academic_sessions")
    op.drop_index("ix_subjects_subject_code", table_name="subjects")
    op.drop_index(
        "ix_student_profiles_registration_number_unique", table_name="student_profiles"
    )

    # Step 3: Drop unique constraints
    op.drop_constraint("time_slots_slot_code_key", "time_slots", type_="unique")
    op.drop_constraint("week_days_day_code_key", "week_days", type_="unique")

    # Step 4: Drop id columns from parent tables (no FK references remain)
    op.drop_column("academic_sessions", "id")
    op.drop_column("classroom", "id")
    op.drop_column("subjects", "id")
    op.drop_column("time_slots", "id")
    op.drop_column("week_days", "id")

    # Step 4b: Create new PRIMARY KEY constraints on business code columns
    op.create_primary_key("pk_academic_sessions", "academic_sessions", ["session_code"])
    op.create_primary_key("pk_classroom", "classroom", ["class_code"])
    op.create_primary_key("pk_subjects", "subjects", ["subject_code"])
    op.create_primary_key("pk_time_slots", "time_slots", ["slot_code"])
    op.create_primary_key("pk_week_days", "week_days", ["day_code"])

    # Step 5: Change FK column types from INTEGER to String
    op.alter_column(
        "assignments",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "assignments",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "chat_rooms",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "class_subjects",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "class_subjects",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "class_subjects",
        "subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "class_timetable",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "week_day_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=3),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "time_slot_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),
        existing_nullable=False,
    )

    op.alter_column(
        "classroom",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "daily_classes",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_classes",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "exams",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "exams",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "fees",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "notices",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "notices",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )

    op.alter_column(
        "student_classes",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_classes",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "student_id_cards",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "student_promotion_history",
        "from_session_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_promotion_history",
        "to_session_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_promotion_history",
        "from_classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "student_promotion_history",
        "to_classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "study_materials",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "study_materials",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    op.alter_column(
        "teacher_availability",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_availability",
        "week_day_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=3),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_availability",
        "time_slot_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),
        existing_nullable=False,
    )

    op.alter_column(
        "teacher_subjects",
        "academic_sessions_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_subjects",
        "classroom_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_subjects",
        "subject_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
    )

    # Step 6: Recreate FK constraints pointing to new String PK columns
    op.create_foreign_key(
        "fk_assignments_academic_sessions",
        "assignments",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_assignments_classroom",
        "assignments",
        "classroom",
        ["classroom_id"],
        ["class_code"],
    )

    op.create_foreign_key(
        "fk_chat_rooms_academic_sessions",
        "chat_rooms",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )

    op.create_foreign_key(
        "fk_class_subjects_academic_sessions",
        "class_subjects",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_class_subjects_classroom",
        "class_subjects",
        "classroom",
        ["classroom_id"],
        ["class_code"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_class_subjects_subject",
        "class_subjects",
        "subjects",
        ["subject_id"],
        ["subject_code"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "fk_class_timetable_academic_sessions",
        "class_timetable",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_class_timetable_classroom",
        "class_timetable",
        "classroom",
        ["classroom_id"],
        ["class_code"],
    )
    op.create_foreign_key(
        "fk_class_timetable_time_slot",
        "class_timetable",
        "time_slots",
        ["time_slot_id"],
        ["slot_code"],
    )
    op.create_foreign_key(
        "fk_class_timetable_week_day",
        "class_timetable",
        "week_days",
        ["week_day_id"],
        ["day_code"],
    )

    op.create_foreign_key(
        "fk_classroom_academic_sessions",
        "classroom",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        "fk_daily_classes_academic_sessions",
        "daily_classes",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_daily_classes_classroom",
        "daily_classes",
        "classroom",
        ["classroom_id"],
        ["class_code"],
    )

    op.create_foreign_key(
        "fk_exams_academic_sessions",
        "exams",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_exams_classroom", "exams", "classroom", ["classroom_id"], ["class_code"]
    )

    op.create_foreign_key(
        "fk_fees_academic_sessions",
        "fees",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )

    op.create_foreign_key(
        "fk_notices_academic_sessions",
        "notices",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_notices_classroom", "notices", "classroom", ["classroom_id"], ["class_code"]
    )

    op.create_foreign_key(
        "fk_student_classes_academic_sessions",
        "student_classes",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_student_classes_classroom",
        "student_classes",
        "classroom",
        ["classroom_id"],
        ["class_code"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        "fk_student_id_cards_academic_sessions",
        "student_id_cards",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        "fk_student_promotion_history_from_session",
        "student_promotion_history",
        "academic_sessions",
        ["from_session_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_student_promotion_history_to_session",
        "student_promotion_history",
        "academic_sessions",
        ["to_session_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_student_promotion_history_from_classroom",
        "student_promotion_history",
        "classroom",
        ["from_classroom_id"],
        ["class_code"],
    )
    op.create_foreign_key(
        "fk_student_promotion_history_to_classroom",
        "student_promotion_history",
        "classroom",
        ["to_classroom_id"],
        ["class_code"],
    )

    op.create_foreign_key(
        "fk_study_materials_academic_sessions",
        "study_materials",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_study_materials_classroom",
        "study_materials",
        "classroom",
        ["classroom_id"],
        ["class_code"],
    )

    op.create_foreign_key(
        "fk_teacher_availability_academic_sessions",
        "teacher_availability",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
    )
    op.create_foreign_key(
        "fk_teacher_availability_week_day",
        "teacher_availability",
        "week_days",
        ["week_day_id"],
        ["day_code"],
    )
    op.create_foreign_key(
        "fk_teacher_availability_time_slot",
        "teacher_availability",
        "time_slots",
        ["time_slot_id"],
        ["slot_code"],
    )

    op.create_foreign_key(
        "fk_teacher_subjects_academic_sessions",
        "teacher_subjects",
        "academic_sessions",
        ["academic_sessions_id"],
        ["session_code"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_teacher_subjects_classroom",
        "teacher_subjects",
        "classroom",
        ["classroom_id"],
        ["class_code"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_teacher_subjects_subject",
        "teacher_subjects",
        "subjects",
        ["subject_id"],
        ["subject_code"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("pk_week_days", "week_days", type_="primary")
    op.add_column(
        "week_days", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False)
    )
    op.create_unique_constraint("week_days_day_code_key", "week_days", ["day_code"])
    op.drop_constraint("pk_time_slots", "time_slots", type_="primary")
    op.add_column(
        "time_slots", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False)
    )
    op.create_unique_constraint("time_slots_slot_code_key", "time_slots", ["slot_code"])
    op.drop_constraint(None, "teacher_subjects", type_="foreignkey")
    op.drop_constraint(None, "teacher_subjects", type_="foreignkey")
    op.drop_constraint(None, "teacher_subjects", type_="foreignkey")
    op.create_foreign_key(
        "teacher_subjects_classroom_id_fkey",
        "teacher_subjects",
        "classroom",
        ["classroom_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "teacher_subjects_subject_id_fkey",
        "teacher_subjects",
        "subjects",
        ["subject_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "teacher_subjects_academic_sessions_id_fkey",
        "teacher_subjects",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.alter_column(
        "teacher_subjects",
        "subject_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_subjects",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_subjects",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "teacher_availability", type_="foreignkey")
    op.drop_constraint(None, "teacher_availability", type_="foreignkey")
    op.drop_constraint(None, "teacher_availability", type_="foreignkey")
    op.create_foreign_key(
        "teacher_availability_time_slot_id_fkey",
        "teacher_availability",
        "time_slots",
        ["time_slot_id"],
        ["id"],
    )
    op.create_foreign_key(
        "teacher_availability_week_day_id_fkey",
        "teacher_availability",
        "week_days",
        ["week_day_id"],
        ["id"],
    )
    op.create_foreign_key(
        "teacher_availability_academic_sessions_id_fkey",
        "teacher_availability",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.alter_column(
        "teacher_availability",
        "time_slot_id",
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_availability",
        "week_day_id",
        existing_type=sa.String(length=3),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "teacher_availability",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint("pk_subjects", "subjects", type_="primary")
    op.add_column(
        "subjects", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False)
    )
    op.create_index(
        "ix_subjects_subject_code", "subjects", ["subject_code"], unique=True
    )
    op.drop_constraint(None, "study_materials", type_="foreignkey")
    op.drop_constraint(None, "study_materials", type_="foreignkey")
    op.create_foreign_key(
        "study_materials_academic_sessions_id_fkey",
        "study_materials",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.create_foreign_key(
        "study_materials_classroom_id_fkey",
        "study_materials",
        "classroom",
        ["classroom_id"],
        ["id"],
    )
    op.alter_column(
        "study_materials",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "study_materials",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "student_promotion_history", type_="foreignkey")
    op.drop_constraint(None, "student_promotion_history", type_="foreignkey")
    op.drop_constraint(None, "student_promotion_history", type_="foreignkey")
    op.drop_constraint(None, "student_promotion_history", type_="foreignkey")
    op.create_foreign_key(
        "student_promotion_history_to_session_id_fkey",
        "student_promotion_history",
        "academic_sessions",
        ["to_session_id"],
        ["id"],
    )
    op.create_foreign_key(
        "student_promotion_history_to_classroom_id_fkey",
        "student_promotion_history",
        "classroom",
        ["to_classroom_id"],
        ["id"],
    )
    op.create_foreign_key(
        "student_promotion_history_from_classroom_id_fkey",
        "student_promotion_history",
        "classroom",
        ["from_classroom_id"],
        ["id"],
    )
    op.create_foreign_key(
        "student_promotion_history_from_session_id_fkey",
        "student_promotion_history",
        "academic_sessions",
        ["from_session_id"],
        ["id"],
    )
    op.alter_column(
        "student_promotion_history",
        "to_classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "student_promotion_history",
        "from_classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "student_promotion_history",
        "to_session_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "student_promotion_history",
        "from_session_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.create_index(
        "ix_student_profiles_registration_number_unique",
        "student_profiles",
        ["registration_number"],
        unique=True,
    )
    op.drop_constraint(None, "student_id_cards", type_="foreignkey")
    op.create_foreign_key(
        "student_id_cards_academic_sessions_id_fkey",
        "student_id_cards",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.alter_column(
        "student_id_cards",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "student_classes", type_="foreignkey")
    op.drop_constraint(None, "student_classes", type_="foreignkey")
    op.create_foreign_key(
        "student_classes_academic_sessions_id_fkey",
        "student_classes",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "student_classes_classroom_id_fkey",
        "student_classes",
        "classroom",
        ["classroom_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.alter_column(
        "student_classes",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "student_classes",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "notices", type_="foreignkey")
    op.drop_constraint(None, "notices", type_="foreignkey")
    op.create_foreign_key(
        "notices_academic_sessions_id_fkey",
        "notices",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.create_foreign_key(
        "notices_classroom_id_fkey", "notices", "classroom", ["classroom_id"], ["id"]
    )
    op.alter_column(
        "notices",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    op.alter_column(
        "notices",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "fees", type_="foreignkey")
    op.create_foreign_key(
        "fees_academic_sessions_id_fkey",
        "fees",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.alter_column(
        "fees",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "exams", type_="foreignkey")
    op.drop_constraint(None, "exams", type_="foreignkey")
    op.create_foreign_key(
        "exams_classroom_id_fkey", "exams", "classroom", ["classroom_id"], ["id"]
    )
    op.create_foreign_key(
        "exams_academic_sessions_id_fkey",
        "exams",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.alter_column(
        "exams",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "exams",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "daily_classes", type_="foreignkey")
    op.drop_constraint(None, "daily_classes", type_="foreignkey")
    op.create_foreign_key(
        "daily_classes_classroom_id_fkey",
        "daily_classes",
        "classroom",
        ["classroom_id"],
        ["id"],
    )
    op.create_foreign_key(
        "daily_classes_academic_sessions_id_fkey",
        "daily_classes",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.alter_column(
        "daily_classes",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_classes",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint("pk_classroom", "classroom", type_="primary")
    op.add_column(
        "classroom", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False)
    )
    op.drop_constraint(None, "classroom", type_="foreignkey")
    op.create_foreign_key(
        "classroom_academic_sessions_id_fkey",
        "classroom",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.alter_column(
        "classroom",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "class_timetable", type_="foreignkey")
    op.drop_constraint(None, "class_timetable", type_="foreignkey")
    op.drop_constraint(None, "class_timetable", type_="foreignkey")
    op.drop_constraint(None, "class_timetable", type_="foreignkey")
    op.create_foreign_key(
        "class_timetable_classroom_id_fkey",
        "class_timetable",
        "classroom",
        ["classroom_id"],
        ["id"],
    )
    op.create_foreign_key(
        "class_timetable_week_day_id_fkey",
        "class_timetable",
        "week_days",
        ["week_day_id"],
        ["id"],
    )
    op.create_foreign_key(
        "class_timetable_time_slot_id_fkey",
        "class_timetable",
        "time_slots",
        ["time_slot_id"],
        ["id"],
    )
    op.create_foreign_key(
        "class_timetable_academic_sessions_id_fkey",
        "class_timetable",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.alter_column(
        "class_timetable",
        "time_slot_id",
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "week_day_id",
        existing_type=sa.String(length=3),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "class_timetable",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "class_subjects", type_="foreignkey")
    op.drop_constraint(None, "class_subjects", type_="foreignkey")
    op.drop_constraint(None, "class_subjects", type_="foreignkey")
    op.create_foreign_key(
        "class_subjects_subject_id_fkey",
        "class_subjects",
        "subjects",
        ["subject_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "class_subjects_academic_sessions_id_fkey",
        "class_subjects",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "class_subjects_classroom_id_fkey",
        "class_subjects",
        "classroom",
        ["classroom_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.alter_column(
        "class_subjects",
        "subject_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "class_subjects",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "class_subjects",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "chat_rooms", type_="foreignkey")
    op.create_foreign_key(
        "chat_rooms_academic_sessions_id_fkey",
        "chat_rooms",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.alter_column(
        "chat_rooms",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "assignments", type_="foreignkey")
    op.drop_constraint(None, "assignments", type_="foreignkey")
    op.create_foreign_key(
        "assignments_academic_sessions_id_fkey",
        "assignments",
        "academic_sessions",
        ["academic_sessions_id"],
        ["id"],
    )
    op.create_foreign_key(
        "assignments_classroom_id_fkey",
        "assignments",
        "classroom",
        ["classroom_id"],
        ["id"],
    )
    op.alter_column(
        "assignments",
        "classroom_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "assignments",
        "academic_sessions_id",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_constraint("pk_academic_sessions", "academic_sessions", type_="primary")
    op.add_column(
        "academic_sessions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
    op.create_index(
        "ix_academic_sessions_session_code",
        "academic_sessions",
        ["session_code"],
        unique=True,
    )
