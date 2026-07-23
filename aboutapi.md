# SCHOOL-ERP API Documentation

## Base URL: `/`

---

## 1. Authentication APIs (`/`)

### POST `/login`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | User email |
| password | string (min 8) | User password |

**Access:** `Public` (koi bhi login kar sakta hai)

**Response:** access_token, refresh_token, user details, profile data

---

### POST `/token`
| Field | Type | Description |
|-------|------|-------------|
| username | string | OAuth2 form (email ya phone) |
| password | string | User password |

**Access:** `Public` (Swagger UI ke liye, hidden from docs)

---

### POST `/refresh`
| Field | Type | Description |
|-------|------|-------------|
| refresh_token | string | Refresh token from login |

**Access:** `Public`

---

### POST `/logout`
| Field | Type | Description |
|-------|------|-------------|
| device_token | string (optional) | Device token to clear |
| all_devices | boolean | Sab devices se logout |

**Access:** `All Authenticated Users` (Student, Teacher, Admin)

---

### POST `/change-password`
| Field | Type | Description |
|-------|------|-------------|
| current_password | string (min 8) | Current password |
| new_password | string (min 8) | New password |

**Access:** `All Authenticated Users`

---

### POST `/forgot-password`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | Registered email |

**Access:** `Public`

---

### POST `/reset-password`
| Field | Type | Description |
|-------|------|-------------|
| token | string | Reset token from email |
| new_password | string (min 8) | New password |

**Access:** `Public`

---

### POST `/send-verification-otp`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | User email |

**Access:** `Public`

---

### POST `/verify-email`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | User email |
| otp | string (6 digits) | OTP code |

**Access:** `Public`

---

### POST `/resend-otp`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | User email |

**Access:** `Public`

---

### POST `/send-login-otp`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | User email |

**Access:** `Public`

---

### POST `/verify-login-otp`
| Field | Type | Description |
|-------|------|-------------|
| email | EmailStr | User email |
| otp | string (6 digits) | OTP code |

**Access:** `Public`

**Response:** access_token, refresh_token, user details

---

### GET `/validate-token`
**Access:** `All Authenticated Users`

---

### GET `/health`
**Access:** `Public`

---

## 2. Student APIs (`/student`)

### GET `/student/profile`
**Access:** `Student` (apna profile dekhega)

---

### PUT `/student/profile`
**Fields (optional, jo update karna ho):**
| Field | Type |
|-------|------|
| student_name | string |
| gender | string |
| date_of_birth | date |
| blood_group | string |
| profile_photo | string |
| school_name | string |
| school_address | string |
| medium | string |
| board | string |
| address | string |
| city | string |
| state | string |
| pincode | string |
| parent_name | string |
| parent_phone | string |
| guardian_name | string |
| guardian_phone | string |
| emergency_contact | string |
| admission_date | date |
| remarks | string |

**Access:** `Student` (apna profile update karega)

---

### GET `/student/profile/{student_id}`
**Path Parameter:** student_id (student_id ya email ya naam)

**Access:**
- `Admin` - kisi bhi student ka profile dekh sakta hai
- `Student` - sirf apna profile dekh sakta hai
- `Teacher` - **forbidden (403)**

---

### PUT `/student/profile/{student_id}`
**Path Parameter:** student_id
**Body:** StudentProfileUpdate fields

**Access:** `Student` (sirf apna profile update kar sakta hai)
- Admin aur Teacher ko 403 milega

---

### GET `/student/classes`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (optional) |

**Access:** `Student`

---

### GET `/student/attendance/summary`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |

**Access:** `Student`

---

### GET `/student/attendance/daily`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |
| start_date | datetime (optional) |
| end_date | datetime (optional) |

**Access:** `Student`

---

### GET `/student/assignments`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |
| subject_id | int (optional) |

**Access:** `Student`

---

### GET `/student/exams`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |
| subject_id | int (optional) |

**Access:** `Student`

---

### GET `/student/fees`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |
| status (alias: status) | string (optional) |

**Access:** `Student`

---

### GET `/student/fees/summary`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |

**Access:** `Student`

---

## 3. Teacher APIs (`/teacher`)

### GET `/teacher/profile`
**Access:** `Teacher`

---

### PUT `/teacher/profile`
**Fields (optional):**
| Field | Type |
|-------|------|
| teacher_name | string |
| gender | string |
| date_of_birth | date |
| qualification | string |
| experience_years | float |
| specialization | string |
| profile_photo | string |
| employee_code | string |
| joining_date | date |
| designation | string |
| department | string |
| address | string |
| city | string |
| state | string |
| pincode | string |
| emergency_contact | string |
| remarks | string |

**Access:** `Teacher`

---

### GET `/teacher/profile/{teacher_id}`
**Path Parameter:** teacher_id (teacher_id ya email ya naam)

**Access:**
- `Admin` - kisi bhi teacher ka profile dekh sakta hai
- `Teacher` - sirf apna profile dekh sakta hai
- `Student` - **forbidden (403)**

---

### PUT `/teacher/profile/{teacher_id}`
**Path Parameter:** teacher_id
**Body:** TeacherProfileUpdate fields

**Access:** `Teacher` (sirf apna profile update kar sakta hai)

---

### GET `/teacher/classes`
**Query Parameter:** academic_sessions_id (optional)
**Access:** `Teacher`

---

### GET `/teacher/students`
**Query Parameters:**
| Field | Type |
|-------|------|
| classroom_id | int (required) |
| academic_sessions_id | int (required) |

**Access:** `Teacher`

---

### GET `/teacher/my-students`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (required) |
| classroom_id | int (optional) |

**Access:** `Teacher`

---

### GET `/teacher/subjects`
**Query Parameter:** academic_sessions_id (optional)
**Access:** `Teacher`

---

### POST `/teacher/attendance/mark`
**Query Parameter:**
| Field | Type |
|-------|------|
| daily_class_id | int |

**Body (list of objects):**
| Field | Type |
|-------|------|
| student_class_id | int |
| attendance_status | string (default: "Present") |
| is_late | boolean (default: false) |
| late_minutes | int (default: 0) |
| remarks | string (optional) |

**Access:** `Teacher`

---

### GET `/teacher/assignments`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |
| status | string (optional) |

**Access:** `Teacher`

---

### GET `/teacher/dashboard`
**Access:** `Teacher`

---

## 4. Subject APIs (`/subjects`)

### POST `/subjects/`
| Field | Type |
|-------|------|
| subject_code | string |
| subject_name | string |
| description | string (optional) |
| display_order | int (optional) |
| subject_type | string (optional) |

**Access:** `Admin`

---

### GET `/subjects/`
**Query Parameters:**
| Field | Type |
|-------|------|
| is_active | bool (optional) |
| subject_type | string (optional) |

**Access:** `All Authenticated Users`

---

### GET `/subjects/{subject_id}`
**Access:** `All Authenticated Users`

---

### PUT `/subjects/{subject_id}`
**Body:** SubjectUpdate fields (optional)
**Access:** `Admin`

---

### DELETE `/subjects/{subject_id}`
**Access:** `Admin` (soft delete)

---

### POST `/subjects/class-subjects`
| Field | Type |
|-------|------|
| academic_sessions_id | int |
| classroom_id | int |
| subject_id | int |
| display_order | int (optional) |

**Access:** `Admin`

---

### GET `/subjects/class-subjects`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |

**Access:** `All Authenticated Users`

---

### GET `/subjects/classes/{classroom_id}/subjects`
**Query Parameter:** academic_sessions_id (optional)
**Access:** `All Authenticated Users`

---

### DELETE `/subjects/class-subjects/{mapping_id}`
**Access:** `Admin`

---

## 5. Daily Class APIs (`/daily-class`)

### POST `/daily-class/`
| Field | Type |
|-------|------|
| daily_class_id | string (optional) |
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |
| class_subject_id | int (optional) |
| teacher_subject_id | int |
| timetable_id | int (optional) |
| class_date | date |
| topic | string (optional) |
| description | string (optional) |
| homework | string (optional) |
| lecture_status | LectureStatus (optional) |
| started_at | datetime (optional) |
| ended_at | datetime (optional) |
| total_minutes | int (optional) |
| remarks | string (optional) |

**Access:** `Teacher`

---

### GET `/daily-class/classroom/{classroom_id}/summary`
**Query Parameters:**
| Field | Type |
|-------|------|
| start_date | date |
| end_date | date |

**Access:** `All Authenticated Users`

---

### GET `/daily-class/`
**Query Parameters:**
| Field | Type |
|-------|------|
| classroom_id | int (optional) |
| class_date | date (optional) |
| lecture_status | LectureStatus (optional) |

**Access:** `All Authenticated Users`
- Teacher sirf apne classes dekhega
- Admin sab dekhega

---

### GET `/daily-class/{daily_class_id}`
**Access:** `All Authenticated Users`

---

### POST `/daily-class/{daily_class_id}/students`
**Body (list of objects):**
| Field | Type |
|-------|------|
| student_class_id | int |
| attendance_status | AttendanceStatus |
| is_late | bool (optional) |
| late_minutes | int (optional) |
| remarks | string (optional) |

**Access:** `Teacher`

---

### GET `/daily-class/{daily_class_id}/students`
**Access:** `All Authenticated Users`

---

### PUT `/daily-class/{daily_class_id}`
**Body:** DailyClassUpdate fields
**Access:** `Teacher` (sirf apni class)

---

### DELETE `/daily-class/{daily_class_id}`
**Access:** `Teacher` (sirf apni class)

---

## 6. Assignment APIs (`/assignments`)

### POST `/assignments/`
| Field | Type |
|-------|------|
| assignment_id | string (optional) |
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |
| class_subject_id | int (optional) |
| teacher_subject_id | int |
| title | string |
| description | string (optional) |
| instructions | string (optional) |
| due_date | date (optional) |
| due_time | time (optional) |
| total_marks | int (optional) |
| passing_marks | int (optional) |
| file_name | string (optional) |
| file_path | string (optional) |
| file_type | string (optional) |
| file_size | int (optional) |
| status | AssignmentStatus (optional) |
| publish_at | datetime (optional) |
| close_at | datetime (optional) |

**Access:** `Teacher`

---

### GET `/assignments/`
**Query Parameters:**
| Field | Type |
|-------|------|
| classroom_id | int (optional) |
| status | AssignmentStatus (optional) |

**Access:** `All Authenticated Users`

---

### GET `/assignments/{assignment_id}`
**Access:**
- `Admin` - sab dekh sakta hai
- `Teacher` - sirf apne assignments
- `Student` - **permission denied**

---

### PUT `/assignments/{assignment_id}`
**Body:** AssignmentUpdate fields
**Access:** `Teacher` (sirf apna assignment ya Admin)

---

### DELETE `/assignments/{assignment_id}`
**Access:** `Teacher` (sirf apna assignment ya Admin)

---

### POST `/assignments/{assignment_id}/results`
**Body (list of objects):**
| Field | Type |
|-------|------|
| student_class_id | int |
| obtained_marks | float |
| percentage | float |
| grade | string (optional) |
| remarks | string (optional) |

**Access:** `Teacher` (ya Admin)

---

### GET `/assignments/{assignment_id}/results`
**Access:**
- `Admin` - sab dekh sakta hai
- `Teacher` - sirf apne assignments ke results
- `Student` - **permission denied**

---

## 7. Exam APIs (`/exams`)

### POST `/exams/`
| Field | Type |
|-------|------|
| exam_id | string (optional) |
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |
| class_subject_id | int (optional) |
| teacher_subject_id | int |
| exam_name | string |
| exam_type | string (optional) |
| description | string (optional) |
| exam_date | date (optional) |
| start_time | time (optional) |
| end_time | time (optional) |
| duration_minutes | int (optional) |
| room_number | string (optional) |
| total_marks | int (optional) |
| passing_marks | int (optional) |
| status | ExamStatus (optional) |
| publish_at | datetime (optional) |
| completed_at | datetime (optional) |

**Access:** `Teacher`

---

### GET `/exams/`
**Query Parameters:**
| Field | Type |
|-------|------|
| classroom_id | int (optional) |
| status | ExamStatus (optional) |

**Access:** `All Authenticated Users`
- Teacher sirf apne exams dekhega

---

### GET `/exams/{exam_id}`
**Access:** `All Authenticated Users`

---

### PUT `/exams/{exam_id}`
**Body:** ExamUpdate fields
**Access:** `Teacher` (sirf apna exam ya Admin)

---

### DELETE `/exams/{exam_id}`
**Access:** `Teacher` (sirf apna exam ya Admin)

---

### POST `/exams/{exam_id}/results`
**Body (list of objects):**
| Field | Type |
|-------|------|
| student_class_id | int |
| obtained_marks | float |
| percentage | float (optional) |
| grade | string (optional) |
| remarks | string (optional) |
| rank_in_class | int (optional) |
| is_absent | bool (optional) |

**Access:** `Teacher` (ya Admin)

---

### GET `/exams/{exam_id}/results`
**Access:** `All Authenticated Users`

---

## 8. Fee APIs (`/fees`)

### POST `/fees/`
| Field | Type |
|-------|------|
| fee_id | string (optional) |
| academic_sessions_id | int (optional) |
| student_class_id | int |
| fee_month | int |
| fee_year | int |
| total_amount | Decimal |
| paid_amount | Decimal (optional) |
| discount_amount | Decimal (optional) |
| fine_amount | Decimal (optional) |
| due_date | date (optional) |
| paid_date | date (optional) |
| status | FeeStatus (optional) |
| remarks | string (optional) |

**Access:** `Admin`

---

### GET `/fees/`
**Query Parameters:**
| Field | Type |
|-------|------|
| student_class_id | int (optional) |
| status | FeeStatus (optional) |
| fee_month | int (optional) |
| fee_year | int (optional) |

**Access:** `All Authenticated Users`
- Student sirf apne fees dekhega

---

### GET `/fees/{fee_id}`
**Access:** `All Authenticated Users`

---

### PUT `/fees/{fee_id}`
**Body:** FeeUpdate fields
**Access:** `Admin`

---

### DELETE `/fees/{fee_id}`
**Access:** `Admin`

---

### POST `/fees/{fee_id}/pay`
| Field | Type |
|-------|------|
| amount_paid | Decimal |
| payment_date | date (optional) |

**Access:** `All Authenticated Users`
- Student sirf apna fee pay kar sakta hai

---

### GET `/fees/summary/student/{student_id}`
**Path Parameter:** student_id (student_id ya email ya naam)
**Query Parameter:** academic_sessions_id (int)

**Access:** `Admin`

---

## 9. Chat APIs (`/chat`)

### POST `/chat/rooms`
| Field | Type |
|-------|------|
| chat_room_id | string (optional) |
| academic_sessions_id | int (optional) |
| student_class_id | int |
| teacher_subject_id | int |
| last_message | string (optional) |
| last_message_at | datetime (optional) |
| student_unread | int (optional) |
| teacher_unread | int (optional) |

**Access:** `Teacher`

---

### GET `/chat/rooms`
**Access:** `All Authenticated Users`
- Teacher sirf apne rooms
- Student sirf apne rooms
- Admin sab

---

### GET `/chat/rooms/{room_id}`
**Access:** `All Authenticated Users`

---

### PUT `/chat/rooms/{room_id}`
**Body:** ChatRoomUpdate fields
**Access:** `Teacher`, `Admin`

---

### DELETE `/chat/rooms/{room_id}`
**Access:** `Admin`

---

### POST `/chat/rooms/{room_id}/messages`
| Field | Type |
|-------|------|
| message | string |
| attachment_url | string (optional) |

**Access:** `All Authenticated Users`

---

### GET `/chat/rooms/{room_id}/messages`
**Query Parameters:**
| Field | Type |
|-------|------|
| limit | int (default: 50, max: 200) |
| before | datetime (optional) |

**Access:** `All Authenticated Users`

---

### DELETE `/chat/rooms/{room_id}/messages/{message_id}`
**Access:** `All Authenticated Users` (sirf apna message ya Admin)

---

### GET `/chat/unread`
**Access:** `All Authenticated Users`

---

## 10. Dashboard APIs (`/dashboard`)

### GET `/dashboard/student`
**Access:** `Student`

---

### GET `/dashboard/teacher`
**Access:** `Teacher`

---

### GET `/dashboard/admin`
**Access:** `Admin`

---

## 11. Notice APIs (`/notices`)

### POST `/notices/`
| Field | Type |
|-------|------|
| title | string (Form) |
| description | string (Form) |
| notice_type | NoticeType (Form, default: GENERAL) |
| audience | NoticeAudience (Form, default: ALL) |
| publish_date | date (Form) |
| expiry_date | date (Form, optional) |
| is_pinned | bool (Form, default: false) |
| academic_sessions_id | int (Form) |
| classroom_id | int (Form, optional) |
| file | UploadFile (optional) |

**Access:** `Admin`

---

### GET `/notices/`
**Query Parameters:**
| Field | Type |
|-------|------|
| notice_type | NoticeType (optional) |
| audience | NoticeAudience (optional) |
| is_pinned | bool (optional) |

**Access:** `All Authenticated Users`
- Audience filter: Student sirf ALL/STUDENT, Teacher sirf ALL/TEACHER, Admin sab

---

### GET `/notices/{notice_id}`
**Access:** `All Authenticated Users` (audience check)

---

### PUT `/notices/{notice_id}`
**Body (Form fields, all optional):**
| Field | Type |
|-------|------|
| title | string |
| description | string |
| notice_type | NoticeType |
| audience | NoticeAudience |
| publish_date | date |
| expiry_date | date |
| is_pinned | bool |
| classroom_id | int |
| file | UploadFile |

**Access:** `Admin`

---

### DELETE `/notices/{notice_id}`
**Access:** `Admin` (soft delete)

---

### POST `/notices/{notice_id}/pin`
**Access:** `Admin`

---

### POST `/notices/{notice_id}/unpin`
**Access:** `Admin`

---

### GET `/notices/{notice_id}/view`
**Access:** `All Authenticated Users` (audience check)

---

### GET `/notices/{notice_id}/download`
**Access:** `All Authenticated Users` (audience check)

---

## 12. Admin APIs (`/admin`)

### POST `/admin/user`
| Field | Type |
|-------|------|
| email | EmailStr |
| phone | string (10-15 digits) |
| role | UserRole (ADMIN, TEACHER, STUDENT) |
| password | string (min 8) |

**Access:** `Admin`

---

### GET `/admin/user`
**Query Parameters:**
| Field | Type |
|-------|------|
| page | int (default: 1) |
| page_size | int (default: 20, max: 100) |
| role | UserRole (optional) |
| is_active | bool (optional) |
| search | string (optional) |

**Access:** `Admin`

---

### GET `/admin/user/{user_id}`
**Access:** `Admin`

---

### PUT `/admin/user/{user_id}`
| Field | Type |
|-------|------|
| email | EmailStr (optional) |
| phone | string (optional) |
| profile_photo | string (optional) |
| is_active | bool (optional) |
| device_token | string (optional) |

**Access:** `Admin`

---

### DELETE `/admin/user/{user_id}`
**Query Parameter:** soft_delete (bool, default: true)
**Access:** `Admin` (apne aap ko delete nahi kar sakta)

---

### GET `/admin/admin-profiles`
**Access:** `Admin`

---

### POST `/admin/academic-sessions`
| Field | Type |
|-------|------|
| session_code | string |
| session_name | string |
| start_year | int |
| end_year | int |
| start_date | date (optional) |
| end_date | date (optional) |
| is_current | bool (optional) |
| description | string (optional) |

**Access:** `Admin`

---

### GET `/admin/academic-sessions`
**Query Parameter:** is_current (bool, optional)
**Access:** `All Authenticated Users`

---

### POST `/admin/classrooms`
| Field | Type |
|-------|------|
| academic_sessions_id | int |
| class_code | string |
| class_name | string |
| section | string |
| display_name | string (optional) |
| description | string (optional) |
| class_teacher_id | string (teacher_id ya email ya naam) |

**Access:** `Admin`

---

### GET `/admin/classrooms`
**Query Parameter:** academic_sessions_id (int, optional)
**Access:** `All Authenticated Users`

---

### POST `/admin/subjects`
| Field | Type |
|-------|------|
| subject_code | string |
| subject_name | string |
| description | string (optional) |
| display_order | int (optional) |
| subject_type | string (optional) |

**Access:** `Admin`

---

### GET `/admin/subjects`
**Query Parameter:** is_active (bool, optional)
**Access:** `All Authenticated Users`

---

### POST `/admin/teacher-subjects`
| Field | Type |
|-------|------|
| academic_sessions_id | int |
| class_subject_id | int |
| classroom_id | int |
| subject_id | int |
| teacher_id | string (teacher_id ya email ya naam) |
| is_class_teacher | bool (optional) |
| remarks | string (optional) |

**Access:** `Admin`

---

### GET `/admin/teacher-subjects`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |
| teacher_id | string (optional) |

**Access:** `Admin`

---

### POST `/admin/student-classes`
| Field | Type |
|-------|------|
| academic_sessions_id | int |
| student_id | string (student_id ya email ya naam) |
| classroom_id | int |
| roll_number | int |
| admission_date | date (optional) |
| status | string (optional) |
| roll_number_locked | bool (optional) |
| remarks | string (optional) |

**Access:** `Admin`

---

### GET `/admin/student-classes`
**Query Parameters:**
| Field | Type |
|-------|------|
| academic_sessions_id | int (optional) |
| classroom_id | int (optional) |
| student_id | string (optional) |

**Access:** `Admin`

---

### GET `/admin/student-profiles`
**Access:** `Admin`

---

### GET `/admin/teacher-profiles`
**Access:** `Admin`

---

### GET `/admin/system/health`
**Access:** `Admin`

---

### GET `/admin/teachers`
**Query Parameters:**
| Field | Type |
|-------|------|
| page | int (default: 1) |
| page_size | int (default: 20, max: 100) |
| search | string (optional) |
| is_active | bool (optional) |
| department | string (optional) |

**Access:** `Admin`

---

### GET `/admin/students`
**Query Parameters:**
| Field | Type |
|-------|------|
| page | int (default: 1) |
| page_size | int (default: 20, max: 100) |
| search | string (optional) |
| class_id | int (optional) |
| class_code | string (optional) |

**Access:** `Admin`

---

### GET `/admin/system/statistics`
**Access:** `Admin`

---

## 13. Admin Directory APIs (`/`)

### GET `/students`
**Query Parameters:**
| Field | Type |
|-------|------|
| page | int (default: 1) |
| page_size | int (default: 20, max: 100) |
| search | string (optional) |
| class_id | int (optional) |
| class_code | string (optional) |
| section | string (optional) |
| status | string (optional) |

**Access:** `Admin`

---

### GET `/teachers`
**Query Parameters:**
| Field | Type |
|-------|------|
| page | int (default: 1) |
| page_size | int (default: 20, max: 100) |
| search | string (optional) |
| department | string (optional) |
| subject | string (optional) |
| status | string (optional) |

**Access:** `Admin`

---

## 14. Study Material APIs (`/study-materials`)

### POST `/study-materials`
| Field | Type |
|-------|------|
| title | string |
| description | string (optional) |
| material_type | string (optional) |
| academic_sessions_id | int |
| classroom_id | int |
| class_subject_id | int |
| teacher_subject_id | int |
| file | UploadFile |

**Access:** `Admin`

---

### GET `/study-materials`
**Access:** `All Authenticated Users`

---

### GET `/study-materials/class-subject/{class_subject_id}`
**Access:** `All Authenticated Users`

---

### GET `/study-materials/{id}`
**Access:** `All Authenticated Users`

---

### GET `/study-materials/{id}/view`
**Access:** `Student`, `Teacher`, `Admin`

---

### GET `/study-materials/{id}/download`
**Access:** `Student`, `Teacher`, `Admin`

---

### PUT `/study-materials/{id}`
**Fields (Form, all optional):**
| Field | Type |
|-------|------|
| title | string |
| description | string |
| material_type | string |
| academic_sessions_id | int |
| classroom_id | int |
| class_subject_id | int |
| teacher_subject_id | int |
| file | UploadFile |

**Access:** `Admin`

---

### DELETE `/study-materials/{id}`
**Access:** `Admin`

---

## 15. Timetable APIs (`/`)

### GET `/weekdays`
**Access:** `All Authenticated Users`

---

### POST `/weekdays`
| Field | Type |
|-------|------|
| day_name | string |
| day_code | string (optional) |
| display_order | int (optional) |
| is_active | bool (optional) |

**Access:** `Admin`

---

### GET `/timeslots`
**Access:** `All Authenticated Users`

---

### POST `/timeslots`
| Field | Type |
|-------|------|
| slot_name | string |
| start_time | time |
| end_time | time |
| display_order | int (optional) |
| is_active | bool (optional) |

**Access:** `Admin`

---

### GET `/timetable/class/{classroom_id}`
**Query Parameter:** session_id (int, required)
**Access:** `All Authenticated Users`

---

### GET `/timetables`
**Query Parameters:**
| Field | Type |
|-------|------|
| class | int (optional) |
| teacher | int (optional) |
| subject | int (optional) |
| day | int (optional) |

**Access:** `Admin`

---

### POST `/timetable`
| Field | Type |
|-------|------|
| academic_sessions_id | int |
| classroom_id | int |
| class_subject_id | int |
| teacher_subject_id | int |
| week_day_id | int |
| time_slot_id | int |
| room_number | string (optional) |
| is_active | bool (optional) |

**Access:** `Admin`

---

### PUT `/timetable/{id}`
**Body:** ClassTimeTableUpdate
**Access:** `Admin`

---

### DELETE `/timetable/{id}`
**Access:** `Admin`

---

### GET `/student/timetable`
**Access:** `Student` (sirf apna timetable)

---

### GET `/teacher/timetable`
**Access:** `Teacher` (sirf apne assigned classes ka timetable)

---

### GET `/availability/teacher/{teacher_subject_id}`
**Query Parameter:** session_id (int, required)
**Access:** `Teacher`

---

### POST `/availability`
| Field | Type |
|-------|------|
| teacher_subject_id | int |
| week_day_id | int |
| time_slot_id | int |
| is_available | bool (optional) |
| remarks | string (optional) |

**Access:** `Teacher`

---

### PUT `/availability/{availability_id}`
**Body:** TeacherAvailabilityUpdate
**Access:** `Teacher`

---

## 16. Student ID Card APIs (`/student`)

### POST `/student/id-card/{student_id}`
**Path Parameter:** student_id (student_id ya email ya naam)
**Query Parameter:** regenerate (bool, default: false)

**Access:** `Admin`

---

### GET `/student/id-card/{student_id}`
**Path Parameter:** student_id (student_id ya email ya naam)

**Access:**
- `Admin` - sab
- `Teacher` - sab
- `Student` - sirf apna

---

### GET `/student/id-card/{student_id}/download`
**Path Parameter:** student_id (student_id ya email ya naam)
**Access:** `All Authenticated Users`

---

### GET `/student/id-card/all`
**Query Parameters:**
| Field | Type |
|-------|------|
| page | int (default: 1) |
| page_size | int (default: 20, max: 100) |

**Access:** `Admin`

---

## 17. Attachment APIs (`/attachments`)

### POST `/attachments/upload`
| Field | Type |
|-------|------|
| entity_type | string |
| entity_id | int |
| file_name | string |
| mime_type | string |
| file_data | string (base64) |

**Access:** `All Authenticated Users`

---

### GET `/attachments/{attachment_id}`
**Access:** `All Authenticated Users`

---

### GET `/attachments/entity/{entity_type}/{entity_id}`
**Access:** `All Authenticated Users`

---

### PUT `/attachments/{attachment_id}`
| Field | Type |
|-------|------|
| file_name | string (optional) |
| mime_type | string (optional) |

**Access:** `All Authenticated Users` (sirf apna ya Admin)

---

### DELETE `/attachments/{attachment_id}`
**Access:** `All Authenticated Users` (sirf apna ya Admin)

---

## 18. Student Search API (`/students/search`)

### GET `/students/search`
**Query Parameters:**
| Field | Type |
|-------|------|
| q | string (search query) |
| limit | int (default: result limit, max: max limit) |

**Access:** `Admin`, `Teacher`

---

## 19. Teacher Search API (`/teachers/search`)

### GET `/teachers/search`
**Query Parameters:**
| Field | Type |
|-------|------|
| q | string (search query) |
| limit | int (default: result limit, max: max limit) |

**Access:** `Admin`

---

## 20. Universal Search API (`/search`)

### GET `/search/universal`
**Query Parameters:**
| Field | Type |
|-------|------|
| q | string (search query) |
| limit | int (default: 5, max: 20) |

**Access:** `Admin`, `Teacher`

---

### GET `/search/classrooms`
**Query Parameters:**
| Field | Type |
|-------|------|
| q | string |
| limit | int (default: 10, max: 50) |

**Access:** `All Authenticated Users`

---

### GET `/search/notices`
**Query Parameters:**
| Field | Type |
|-------|------|
| q | string |
| limit | int (default: 10, max: 50) |

**Access:** `All Authenticated Users`

---

### GET `/search/subjects`
**Query Parameters:**
| Field | Type |
|-------|------|
| q | string |
| limit | int (default: 10, max: 50) |

**Access:** `All Authenticated Users`

---

## 21. Zoom APIs (`/zoom`)

### Meetings CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/meetings[/{uuid}]`
**Access:** `Admin` (sab)

**ZoomMeeting fields:**
| Field | Type |
|-------|------|
| uuid | string |
| meeting_id | int (optional) |
| topic | string (optional) |
| host_id | string (optional) |
| start_time | datetime (optional) |
| duration | int (optional) |
| timezone | string (optional) |
| agenda | string (optional) |
| recording_count | int (optional) |
| share_url | string (optional) |

---

### Recordings CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/recordings[/{id}]`
**Access:** `Admin`

---

### Files CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/files[/{id}]`
**Access:** `Admin`

---

### Transcripts CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/transcripts[/{id}]`
**Access:** `Admin`

---

### Interactions CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/interactions[/{id}]`
**Access:** `Admin`

---

### Duration Reports CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/duration-reports[/{id}]`
**Access:** `Admin`

---

### Interaction Reports CRUD
**Endpoints:** GET, POST, PUT, DELETE `/zoom/interaction-reports[/{id}]`
**Access:** `Admin`

---

## 22. Topic APIs (`/topics`)

### GET `/topics/progress`
**Query Parameters:**
| Field | Type |
|-------|------|
| student_id | int (optional) |
| topic_id | int (optional) |

**Access:** `All Authenticated Users`

---

### POST `/topics/progress`
| Field | Type |
|-------|------|
| student_id | int |
| topic_id | int |
| date | date (optional) |
| progress_percentage | float (optional) |
| status | string (optional) |

**Access:** `Admin`, `Teacher`

---

### GET `/topics/progress/{id}`
**Access:** `All Authenticated Users`

---

### PUT `/topics/progress/{id}`
**Body:** TopicProgressCreate
**Access:** `Admin`, `Teacher`

---

### DELETE `/topics/progress/{id}`
**Access:** `Admin`

---

### GET `/topics/progress-reports`
**Access:** `All Authenticated Users`

---

### POST `/topics/progress-reports`
**Body:** StudentTopicProgressReportCreate
**Access:** `Admin`

---

### GET `/topics/progress-reports/{id}`
**Access:** `All Authenticated Users`

---

### DELETE `/topics/progress-reports/{id}`
**Access:** `Admin`

---

### GET `/topics`
**Query Parameter:** course_id (int, optional)
**Access:** `All Authenticated Users`

---

### POST `/topics`
| Field | Type |
|-------|------|
| topic_id | string |
| topic_name | string (optional) |
| course_id | int (optional) |
| description | string (optional) |
| display_order | int (optional) |

**Access:** `Admin`

---

### GET `/topics/{id}`
**Access:** `All Authenticated Users`

---

### PUT `/topics/{id}`
**Body:** TopicCreate
**Access:** `Admin`

---

### DELETE `/topics/{id}`
**Access:** `Admin`

---

## 23. Khan Academy APIs (`/ka`)

### Courses CRUD
**Endpoints:** GET, POST, PUT, DELETE `/ka/courses[/{id}]`
**Access:**
- GET - `All Authenticated Users`
- POST/PUT/DELETE - `Admin`

---

### Students CRUD
**Endpoints:** GET, POST, PUT, DELETE `/ka/students[/{id}]`
**Access:**
- GET - `All Authenticated Users`
- POST/PUT/DELETE - `Admin`

---

### Reports CRUD
**Endpoints:** GET, POST, PUT, DELETE `/ka/reports[/{id}]`
**Access:**
- GET - `All Authenticated Users`
- POST/PUT/DELETE - `Admin`

---

## 24. Promotion APIs (`/promotions`)

### GET `/promotions`
**Query Parameter:** student_id (string, optional)
**Access:** `Admin`

---

### GET `/promotions/{id}`
**Access:** `Admin`

---

### POST `/promotions`
| Field | Type |
|-------|------|
| student_id | string |
| from_session_id | int |
| to_session_id | int |
| from_classroom_id | int |
| to_classroom_id | int |
| previous_roll_number | int (optional) |
| new_roll_number | int (optional) |
| promotion_date | date (optional) |
| promotion_type | string (optional) |
| remarks | string (optional) |

**Access:** `Admin`

---

### PUT `/promotions/{id}`
**Body:** StudentPromotionHistoryUpdate
**Access:** `Admin`

---

### DELETE `/promotions/{id}`
**Access:** `Admin`

---

## Access Summary Table

| Role | Can Access |
|------|------------|
| **Public** | `/login`, `/token`, `/refresh`, `/forgot-password`, `/reset-password`, `/send-verification-otp`, `/verify-email`, `/resend-otp`, `/send-login-otp`, `/verify-login-otp`, `/health` |
| **Student** | Apna profile, classes, attendance, assignments, exams, fees, timetable, chat (apne rooms), notices (ALL/STUDENT), study materials view/download, attachments |
| **Teacher** | Apna profile, classes, students, subjects, attendance mark, assignments CRUD, exams CRUD, daily class CRUD, chat rooms create, notices (ALL/TEACHER), student search, universal search, study materials view/download |
| **Admin** | Sab kuch - user management, academic sessions, classrooms, subjects, teacher-subject mapping, student enrollment, fees CRUD, notices CRUD, zoom CRUD, topics CRUD, KA CRUD, promotions CRUD, id card generate, all search, system health/statistics |
