class TestStudentDashboard:
    def test_get_student_dashboard(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.get("/dashboard/student", headers=auth_headers_student)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "student" in data
        assert "attendance" in data
        assert "upcoming_assignments" in data
        assert "upcoming_exams" in data
        assert "fees" in data

    def test_student_dashboard_structure(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.get("/dashboard/student", headers=auth_headers_student)
        data = resp.json()
        assert "name" in data["student"]
        assert "student_id" in data["student"]
        assert "total_classes" in data["attendance"]
        assert "present" in data["attendance"]

    def test_student_dashboard_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/dashboard/student", headers=auth_headers_admin)
        assert resp.status_code == 403, resp.text


class TestTeacherDashboard:
    def test_get_teacher_dashboard(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get("/dashboard/teacher", headers=auth_headers_teacher)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "teacher" in data
        assert "summary" in data
        assert "recent_activity" in data

    def test_teacher_dashboard_structure(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get("/dashboard/teacher", headers=auth_headers_teacher)
        data = resp.json()
        assert "name" in data["teacher"]
        assert "total_classes" in data["summary"]
        assert "total_students" in data["summary"]

    def test_teacher_dashboard_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.get("/dashboard/teacher", headers=auth_headers_student)
        assert resp.status_code == 403, resp.text


class TestAdminDashboard:
    def test_get_admin_dashboard(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/dashboard/admin", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "system" in data
        assert "current_session" in data
        assert "recent_activity" in data

    def test_admin_dashboard_system_stats(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/dashboard/admin", headers=auth_headers_admin)
        data = resp.json()
        assert data["system"]["total_user"] >= 1
        assert data["system"]["total_students"] >= 1
        assert data["system"]["total_teachers"] >= 1

    def test_admin_dashboard_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get("/dashboard/admin", headers=auth_headers_teacher)
        assert resp.status_code == 403, resp.text
