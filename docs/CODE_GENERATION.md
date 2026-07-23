# Code Generation Logic

Har table ke primary key (PK) ke liye ek unique code auto-generate hota hai. 
Sabhi codes ka pattern same hai: `{PREFIX}-{RANDOM_8_CHARS}`

## Random Code

```python
def random_code(length=6):
    alphabet = string.ascii_uppercase + string.digits  # A-Z, 0-9
    return "".join(secrets.choice(alphabet) for _ in range(length))
```

Har code 8 random uppercase alphanumeric characters se banta hai (except receipt jo 10 uses karta hai).

## Table-wise Code Prefixes

| Table (Model) | PK Column | Prefix | Example | Generator Function |
|---|---|---|---|---|
| users (User) | `user_code` | `USR-` | `USR-A7K2M9X1` | `generate_user_code()` |
| fees (Fee) | `fee_code` | `FEE-` | `FEE-B3R8T5W2` | `generate_fee_code()` |
| exams (Exam) | `exam_code` | `EXAM-` | `EXAM-P6Q1Z4N8` | `generate_exam_code()` |
| exam_results (ExamResult) | `exam_result_code` | `EXR-` | `EXR-C9V2M6K3` | `generate_exam_result_code()` |
| assignments (Assignment) | `assignment_code` | `ASN-` | `ASN-J7H4R1T9` | `generate_assignment_code()` |
| assignment_results (AssignmentResult) | `assignment_result_code` | `ASR-` | `ASR-D5P8B2W6` | `generate_assignment_result_code()` |
| notices (Notice) | `notice_code` | `NTC-` | `NTC-L3X7V4G1` | `generate_notice_code()` |
| study_materials (StudyMaterial) | `material_code` | `MAT-` | `MAT-F9K2R6Z4` | `generate_material_code()` |
| chat_rooms (ChatRoom) | `chat_room_code` | `CHT-` | `CHT-A1M5J8B3` | `generate_chat_room_code()` |
| chat_messages (ChatMessage) | `chat_message_code` | `MSG-` | `MSG-T7P2W4N9` | `generate_chat_message_code()` |
| class_subjects (ClassSubject) | `class_subject_code` | `CLS-` | `CLS-G6K1R8X3` | `generate_class_subject_code()` |
| teacher_subjects (TeacherSubject) | `teacher_subject_code` | `TCH-` | `TCH-D4P9M2V7` | `generate_teacher_subject_code()` |
| student_classes (StudentClass) | `student_class_code` | `STC-` | `STC-H3B7N1Z5` | `generate_student_class_code()` |
| class_timetable (ClassTimeTable) | `timetable_code` | `TMT-` | `TMT-F8J2K6R4` | `generate_timetable_code()` |
| teacher_availability (TeacherAvailability) | `availability_code` | `AVL-` | `AVL-L9X3P7V1` | `generate_availability_code()` |
| daily_classes (DailyClass) | `daily_class_code` | `DCL-` | `DCL-A5R8T2W6` | `generate_daily_class_code()` |
| daily_class_students (DailyClassStudent) | `daily_class_student_code` | `DCS-` | `DCS-M4J7K1B9` | `generate_daily_class_student_code()` |
| student_attendance (StudentAttendance) | `attendance_code` | `ATT-` | `ATT-G3P8R2X5` | `generate_attendance_code()` |
| student_promotion_history (StudentPromotionHistory) | `promotion_code` | `PRM-` | `PRM-N7H2J6Z4` | `generate_promotion_code()` |
| student_id_cards (StudentIDCard) | `id_card_code` | `IDC-` | `IDC-T9R3K1M5` | `generate_id_card_code()` |
| student_report (StudentReport) | `report_code` | `RPT-` | `RPT-B6D2X4P8` | `generate_report_code()` |
| attachments (Attachment) | `attachment_code` | `ATC-` | `ATC-A7K9M3R1` | `generate_attachment_code()` |
| ka_course (KaCourse) | `ka_course_code` | `KAC-` | `KAC-M8J4B1T6` | `generate_ka_course_code()` |
| ka_student (KaStudent) | `ka_student_code` | `KAS-` | `KAS-D3P7V9R2` | `generate_ka_student_code()` |
| ka_topic (Topic) | `topic_code` | `TOP-` | `TOP-X5K1N8Z3` | `generate_topic_code()` |
| ka_topic_progress (TopicProgress) | `topic_progress_code` | `TPR-` | `TPR-C7R4M2J9` | `generate_topic_progress_code()` |
| student_topic_progress_report (StudentTopicProgressReport) | `topic_progress_report_code` | `TPR-` | `TPR-G8K3R1X6` | `generate_topic_progress_report_code()` |
| zoom_file (ZoomFile) | `zoom_file_code` | `ZFL-` | `ZFL-P5V9D2M4` | `generate_zoom_file_code()` |
| zoom_transcript (ZoomTranscript) | `zoom_transcript_code` | `ZTR-` | `ZTR-A6K2R8J4` | `generate_zoom_transcript_code()` |
| zoom_student_interaction (ZoomStudentInteraction) | `zoom_interaction_code` | `ZIN-` | `ZIN-M9F3B7T1` | `generate_zoom_interaction_code()` |
| zoom_duration_report (ZoomDurationReport) | `duration_report_code` | `ZDR-` | `ZDR-K5R1X8P3` | `generate_duration_report_code()` |
| zoom_interaction_report (ZoomInteractionReport) | `interaction_report_code` | `ZIR-` | `ZIR-C6J2N9V4` | `generate_interaction_report_code()` |

## Special Codes

In tables ke codes alag logic se generate hote hain:

### User IDs
- `generate_student_id()` → `STU{RANDOM_8}` (16 chars)
- `generate_teacher_id()` → `TCH{RANDOM_8}` (16 chars)
- `generate_admin_id()` → `ADM{RANDOM_8}` (16 chars)
- `generate_admin_code()` → `ADM-{RANDOM_8}` (for AdminProfile PK)

### Subject Code
`generate_subject_code(subject_name, class_name)` → e.g. `EN10` (first 2 letters of subject + class digits)

### Timetable / Availability
- `generate_timetable_id(academic_sessions_id, sequence)` → `TMT-{session_id}-{sequence:06d}`
- `generate_availability_id(academic_sessions_id, sequence)` → `AVL-{session_id}-{sequence:06d}`

### Registration Number
`generate_registration_number(year, sequence)` → `REG-{year}-{sequence:05d}`

### Receipt Number
`generate_receipt_no()` → `RCT-{RANDOM_10}`

## UUID Tables

Kuch tables simple UUID v4 use karti hain (random, no prefix):
- `zoom_meeting` → `uuid` (external)
- `zoom_recording_file` → `id` (external)

## Code Uniqueness

Har code:
- Primary key ke tor par use hota hai (VARCHAR(30))
- Secrets.choice() se secure random generate hota hai
- Collision probability negligible hai (26 uppercase + 10 digits = 36^8 ≈ 2.8 trillion combinations)
