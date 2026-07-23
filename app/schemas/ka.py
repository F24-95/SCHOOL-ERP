from datetime import datetime

from .common import BaseSchema


class KaCourseBase(BaseSchema):
    course_name: str | None = None
    course_id: str | None = None


class KaCourseCreate(BaseSchema):
    course_name: str | None = None
    course_id: str


class KaCourseResponse(KaCourseBase):
    business_id: str


class KaStudentBase(BaseSchema):
    student_name: str | None = None
    email: str | None = None


class KaStudentCreate(BaseSchema):
    student_name: str | None = None
    email: str | None = None


class KaStudentResponse(KaStudentBase):
    business_id: str


class StudentReportBase(BaseSchema):
    student_id: str | None = None
    report_type: str | None = None
    created_at: datetime | None = None


class StudentReportCreate(BaseSchema):
    student_id: str | None = None
    report_type: str | None = None


class StudentReportResponse(StudentReportBase):
    business_id: str
