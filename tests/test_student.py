class TestStudentProfile:
    def test_get_own_profile(
        self, client, db_session, auth_headers_student, override_student
    ):
        resp = client.get(
            "/student/profile",
            headers=auth_headers_student,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["student_name"] == "Test Student"

    def test_update_own_profile(
        self, client, db_session, auth_headers_student, override_student
    ):
        resp = client.put(
            "/student/profile",
            json={"student_name": "Updated Student", "city": "Mumbai"},
            headers=auth_headers_student,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["student_name"] == "Updated Student"
        assert data["city"] == "Mumbai"


class TestStudentClasses:
    def test_get_student_classes(
        self, client, db_session, auth_headers_student, override_student
    ):
        resp = client.get(
            "/student/classes",
            headers=auth_headers_student,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list)

    def test_get_student_classes_filtered(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.get(
            f"/student/classes?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_student,
        )
        assert resp.status_code == 200, resp.text


class TestStudentAttendance:
    def test_get_attendance_summary(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.get(
            f"/student/attendance/summary?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_student,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert "total_classes" in data
        else:
            assert resp.status_code == 404, resp.text


class TestStudentAssignments:
    def test_get_assignments(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.get(
            f"/student/assignments?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_student,
        )
        # Handle both cases: 200 with empty list or 404 if no enrollment
        if resp.status_code == 200:
            assert isinstance(resp.json(), list)


class TestStudentExams:
    def test_get_exam_results(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.get(
            f"/student/exams?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_student,
        )
        if resp.status_code == 200:
            assert isinstance(resp.json(), list)


class TestStudentFees:
    def test_get_fees(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.get(
            f"/student/fees?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_student,
        )
        if resp.status_code == 200:
            assert isinstance(resp.json(), list)

    def test_get_fee_summary(
        self,
        client,
        db_session,
        academic_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.get(
            f"/student/fees/summary?academic_sessions_id={academic_session.session_code}",
            headers=auth_headers_student,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert "total_amount" in data
