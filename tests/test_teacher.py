class TestTeacherProfile:
    def test_get_own_profile(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/teacher/profile",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["teacher_name"] == "Test Teacher"

    def test_update_own_profile(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.put(
            "/teacher/profile",
            json={
                "teacher_name": "Updated Teacher",
                "designation": "Head of Department",
                "department": "Mathematics",
            },
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["designation"] == "Head of Department"


class TestTeacherClasses:
    def test_get_assigned_classes(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            "/teacher/classes",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        if len(data) > 0:
            assert "class_code" in data[0]

    def test_get_assigned_classes_filtered(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            f"/teacher/classes?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text


class TestTeacherStudents:
    def test_get_class_students(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            f"/teacher/students?classroom_id={classroom.class_code}&academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_teacher,
        )
        assert resp.status_code in (200, 403), resp.text

    def test_get_my_students(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            f"/teacher/my-students?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list)


class TestTeacherSubjects:
    def test_get_teacher_subjects(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/teacher/subjects",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        if len(data) > 0:
            assert "teacher_subject_code" in data[0]

    def test_get_teacher_subjects_filtered(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            f"/teacher/subjects?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text


class TestTeacherDashboard:
    def test_get_dashboard(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/teacher/dashboard",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "total_classes" in data
        assert "total_students" in data


class TestTeacherAssignments:
    def test_get_assignments(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/teacher/assignments",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)


class TestTeacherAuthorization:
    def test_teacher_cannot_access_student_endpoints(
        self,
        client,
        db_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            "/student/profile",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 403, resp.text
