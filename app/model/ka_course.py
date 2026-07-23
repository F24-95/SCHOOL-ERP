from sqlalchemy import Column, String

from app.api.database import Base
from app.helpers.code_generators import generate_ka_course_id


class KaCourse(Base):
    __tablename__ = "ka_course"

    business_id = Column(String(30), primary_key=True, default=generate_ka_course_id)
    course_name = Column(String(200), nullable=True)
    course_id = Column(String(100), unique=True, nullable=True)
