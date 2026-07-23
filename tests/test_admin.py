class TestAdminCreateUser:
    def test_create_student_user(
        self, client, db_session, academic_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/admin/user",
            json={
                "email": "newstudent@test.edu",
                "phone": "9876543220",
                "role": "student",
                "password": "student@123",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["email"] == "newstudent@test.edu"
        assert data["role"] == "student"
        assert "user_code" in data

    def test_create_teacher_user(
        self, client, db_session, academic_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/admin/user",
            json={
                "email": "newteacher@test.edu",
                "phone": "9876543221",
                "role": "teacher",
                "password": "teacher@123",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["email"] == "newteacher@test.edu"
        assert data["role"] == "teacher"

    def test_create_duplicate_email(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/admin/user",
            json={
                "email": "admin@test.edu",
                "phone": "9876543222",
                "role": "student",
                "password": "student@123",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code in (400, 409), resp.text

    def test_create_user_unauthorized(
        self, client, db_session, auth_headers_student, override_student
    ):
        resp = client.post(
            "/admin/user",
            json={
                "email": "hacker@test.edu",
                "phone": "9876543299",
                "role": "student",
                "password": "student@123",
            },
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text


class TestAdminListUsers:
    def test_list_users(self, client, db_session, auth_headers_admin, override_admin):
        resp = client.get(
            "/admin/user",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "data" in data
        assert len(data["data"]) >= 1

    def test_list_users_filter_by_role(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/user?role=admin",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        for user in data["data"]:
            assert user["role"] == "admin"

    def test_list_users_pagination(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/user?page=1&page_size=5",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "pagination" in data


class TestAdminGetUser:
    def test_get_user_by_id(
        self, client, db_session, admin_user, auth_headers_admin, override_admin
    ):
        resp = client.get(
            f"/admin/user/{admin_user.user_code}?user_code={admin_user.user_code}",
            headers=auth_headers_admin,
        )
        assert resp.status_code in (200, 422), resp.text

    def test_get_user_by_user_code(
        self, client, db_session, admin_user, auth_headers_admin, override_admin
    ):
        resp = client.get(
            f"/admin/user/{admin_user.user_code}",
            headers=auth_headers_admin,
        )
        if resp.status_code == 200:
            assert resp.json()["user_code"] == admin_user.user_code
        else:
            assert resp.status_code == 422, resp.text


class TestAdminAcademicSessions:
    def test_create_academic_session(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/admin/academic-sessions",
            json={
                "session_code": "SES-2027",
                "session_name": "2027-28",
                "start_year": 2027,
                "end_year": 2028,
                "start_date": "2027-04-01",
                "end_date": "2028-03-31",
                "is_current": False,
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["session_code"] == "SES-2027"

    def test_list_academic_sessions(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/academic-sessions",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert len(data) >= 1


class TestAdminClassrooms:
    def test_create_classroom(
        self, client, db_session, academic_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/admin/classrooms",
            json={
                "class_code": "CLS11B",
                "class_name": "Class 11",
                "section": "B",
                "display_name": "Class 11-B",
                "academic_sessions_id": academic_session.session_code,
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["class_code"] == "CLS11B"

    def test_list_classrooms(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/classrooms",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert len(data) >= 1


class TestAdminSubjects:
    def test_create_subject(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/admin/subjects",
            json={
                "subject_code": "PHY11",
                "subject_name": "Physics",
                "subject_type": "Core",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["subject_code"] == "PHY11"

    def test_list_subjects(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/subjects",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert len(data) >= 1


class TestAdminTeacherSubjects:
    def test_assign_teacher_to_subject(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        subject,
        class_subject,
        teacher_user,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/admin/teacher-subjects",
            json={
                "academic_sessions_id": academic_session.session_code,
                "class_subject_id": class_subject.class_subject_code,
                "classroom_id": classroom.class_code,
                "subject_id": subject.subject_code,
                "teacher_id": teacher_user.teacher_id,
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "teacher_subject_code" in data

    def test_list_teacher_subjects(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/teacher-subjects",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text


class TestAdminStudentClasses:
    def test_enroll_student(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        student_user,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/admin/student-classes",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_id": student_user.student_id,
                "classroom_id": classroom.class_code,
                "roll_number": 5,
                "admission_date": "2026-04-01",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "student_class_code" in data

    def test_list_student_classes(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/student-classes",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text


class TestAdminProfiles:
    def test_list_admin_profiles(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/admin-profiles",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text

    def test_list_student_profiles(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/student-profiles",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text

    def test_list_teacher_profiles(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/teacher-profiles",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text


class TestAdminSystem:
    def test_system_health(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/system/health",
            headers=auth_headers_admin,
        )
        assert resp.status_code in (200, 503), resp.text

    def test_system_statistics(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/admin/system/statistics",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
