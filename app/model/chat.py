from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.api.database import Base
from app.core.constants import MAX_CODE_LENGTH
from app.core.mixins import ActiveMixin, TimestampMixin
from app.helpers.code_generators import generate_chat_message_id, generate_chat_room_id

# ============================================================
# AUTO TABLENAME
# ============================================================


# ============================================================
# CHATROOM TABLE
# ============================================================


class ChatRoom(Base, TimestampMixin, ActiveMixin):
    __tablename__ = "chat_rooms"

    business_id = Column(String(30), primary_key=True, default=generate_chat_room_id)

    academic_sessions_id = Column(
        String(MAX_CODE_LENGTH),
        ForeignKey("academic_sessions.session_code"),
        nullable=False,
        index=True,
    )

    student_class_id = Column(
        String(30),
        ForeignKey("student_classes.business_id"),
        nullable=False,
        index=True,
    )

    teacher_subject_id = Column(
        String(30),
        ForeignKey("teacher_subjects.business_id"),
        nullable=False,
        index=True,
    )

    last_message = Column(String(500))

    last_message_at = Column(DateTime)

    student_unread = Column(Integer, default=0, nullable=False)

    teacher_unread = Column(Integer, default=0, nullable=False)

    academic_sessions = relationship("AcademicSession")

    student_class = relationship("StudentClass")

    teacher_subject = relationship("TeacherSubject")

    messages = relationship(
        "ChatMessage",
        back_populates="chat_room",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("student_class_id", "teacher_subject_id", name="uq_chat_room"),
        Index("idx_chat_room", "teacher_subject_id", "student_class_id"),
    )


# ============================================================
# CHATMESSAGE TABLE
# ============================================================


class ChatMessage(Base, TimestampMixin, ActiveMixin):
    __tablename__ = "chat_messages"

    business_id = Column(String(30), primary_key=True, default=generate_chat_message_id)

    chat_room_id = Column(
        String(30),
        ForeignKey("chat_rooms.business_id"),
        nullable=False,
        index=True,
    )

    sender_id = Column(
        String(30),
        ForeignKey("users.business_id"),
        nullable=False,
        index=True,
    )

    message = Column(Text, nullable=False)

    is_edited = Column(Boolean, default=False)

    edited_at = Column(DateTime)

    chat_room = relationship("ChatRoom", back_populates="messages")

    sender = relationship("User")

    __table_args__ = (Index("idx_chat_message", "chat_room_id", "created_at"),)
