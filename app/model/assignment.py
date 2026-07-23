from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.api.database import Base
from app.core.constants import MAX_CODE_LENGTH
from app.core.enums import AssignmentStatus
from app.core.mixins import ActiveMixin, TimestampMixin
from app.helpers.code_generators import (
    generate_assignment_id,
    generate_assignment_result_id,
)

# ============================================================
# AUTO TABLENAME
# ============================================================


# ============================================================
# ASSIGNMENT TABLE
# ============================================================


class Assignment(Base, TimestampMixin, ActiveMixin):
    __tablename__ = "assignments"

    @hybrid_property
    def id(self):
        return self.business_id

    @id.expression
    def id(cls):
        return cls.business_id

    business_id = Column(String(30), primary_key=True, default=generate_assignment_id)

    # =====================================================
    # Academic
    # =====================================================

    academic_sessions_id = Column(
        String(MAX_CODE_LENGTH),
        ForeignKey("academic_sessions.session_code"),
        nullable=False,
        index=True,
    )

    classroom_id = Column(
        String(30),
        ForeignKey("classroom.class_code"),
        nullable=False,
        index=True,
    )

    class_subject_id = Column(
        String(30),
        ForeignKey("class_subjects.business_id"),
        nullable=False,
        index=True,
    )

    teacher_subject_id = Column(
        String(30),
        ForeignKey("teacher_subjects.business_id"),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Assignment
    # =====================================================

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    instructions = Column(Text, nullable=True)

    due_date = Column(Date, nullable=False, index=True)

    due_time = Column(Time, nullable=True)

    total_marks = Column(Float, nullable=False, default=0)

    passing_marks = Column(Float, nullable=False, default=0)

    # =====================================================
    # Attachment (Uploaded File)
    # =====================================================

    file_name = Column(String(255), nullable=True)

    file_path = Column(String(500), nullable=True)

    file_type = Column(String(100), nullable=True)

    file_size = Column(Integer, nullable=True)

    uploaded_by = Column(String(30), ForeignKey("users.business_id"), nullable=True)

    # =====================================================
    # Status
    # =====================================================

    status = Column(
        SAEnum(AssignmentStatus),
        nullable=False,
        default=AssignmentStatus.DRAFT,
        index=True,
    )

    publish_at = Column(DateTime, nullable=True)

    close_at = Column(DateTime, nullable=True)

    # =====================================================
    # Statistics
    # =====================================================

    total_students = Column(Integer, default=0)

    checked_students = Column(Integer, default=0)

    # =====================================================
    # Audit
    # =====================================================

    created_by = Column(String(30), ForeignKey("users.business_id"), nullable=False)

    updated_by = Column(String(30), ForeignKey("users.business_id"), nullable=True)

    deleted_by = Column(String(30), ForeignKey("users.business_id"), nullable=True)

    academic_sessions = relationship("AcademicSession")

    classroom = relationship("ClassRoom")

    class_subject = relationship("ClassSubject")

    teacher_subject = relationship("TeacherSubject")

    creator = relationship("User", foreign_keys=[created_by])

    updater = relationship("User", foreign_keys=[updated_by])

    deleter = relationship("User", foreign_keys=[deleted_by])

    results = relationship(
        "AssignmentResult",
        back_populates="assignment",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("class_subject_id", "title", "due_date", name="uq_assignment"),
        Index("idx_assignment_class", "classroom_id", "due_date"),
        Index("idx_assignment_teacher", "teacher_subject_id", "status"),
        Index("idx_assignment_session", "academic_sessions_id", "status"),
    )


# ============================================================
# ASSIGNMENTRESULT TABLE
# ============================================================


class AssignmentResult(Base, TimestampMixin, ActiveMixin):
    __tablename__ = "assignment_results"

    business_id = Column(
        String(30),
        primary_key=True,
        default=generate_assignment_result_id,
    )

    # ===========================================
    # Relations
    # ===========================================

    assignment_id = Column(
        String(30),
        ForeignKey("assignments.business_id"),
        nullable=False,
        index=True,
    )

    student_class_id = Column(
        String(30),
        ForeignKey("student_classes.business_id"),
        nullable=False,
        index=True,
    )

    # ===========================================
    # Marks
    # ===========================================

    obtained_marks = Column(Float, nullable=False, default=0)

    percentage = Column(Float, default=0)

    grade = Column(String(10))

    remarks = Column(Text)

    # ===========================================
    # Status
    # ===========================================

    is_checked = Column(Boolean, default=False, nullable=False)

    checked_at = Column(DateTime)

    # ===========================================
    # Audit
    # ===========================================

    checked_by = Column(String(30), ForeignKey("users.business_id"))

    assignment = relationship("Assignment", back_populates="results")

    student_class = relationship("StudentClass")

    checker = relationship("User")

    __table_args__ = (
        UniqueConstraint(
            "assignment_id",
            "student_class_id",
            name="uq_assignment_result",
        ),
        Index("idx_assignment_result", "student_class_id", "is_checked"),
    )
