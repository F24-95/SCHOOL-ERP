class TestUnifiedSearch:
    def test_universal_search(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/search/universal?q=test", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "query" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_universal_search_empty_query(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/search/universal?q=", headers=auth_headers_admin)
        assert resp.status_code in (400, 422)

    def test_universal_search_unauthorized_student(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.get("/search/universal?q=test", headers=auth_headers_student)
        assert resp.status_code == 403

    def test_search_classrooms(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/search/classrooms?q=class", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json()["results"], list)

    def test_search_notices(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/search/notices?q=test", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json()["results"], list)

    def test_search_subjects(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/search/subjects?q=math", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert isinstance(resp.json()["results"], list)


class TestStudentSearch:
    def test_student_search(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/students/search?q=student", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_student_search_unauthorized_student(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.get("/students/search?q=student", headers=auth_headers_student)
        assert resp.status_code == 403

    def test_student_search_empty_query(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/students/search?q=", headers=auth_headers_admin)
        assert resp.status_code in (400, 422)


class TestTeacherSearch:
    def test_teacher_search(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/teachers/search?q=teacher", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "results" in data

    def test_teacher_search_unauthorized_teacher(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get("/teachers/search?q=teacher", headers=auth_headers_teacher)
        assert resp.status_code == 403

    def test_teacher_search_empty_query(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/teachers/search?q=", headers=auth_headers_admin)
        assert resp.status_code in (400, 422)
