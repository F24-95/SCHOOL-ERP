from sqlalchemy import Column, DateTime, String

from app.api.database import Base
from app.helpers.code_generators import generate_student_report_id


class StudentReport(Base):
    __tablename__ = "student_report"

    business_id = Column(
        String(30),
        primary_key=True,
        default=generate_student_report_id,
    )
    student_id = Column(String(50), nullable=True)
    report_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=True)
