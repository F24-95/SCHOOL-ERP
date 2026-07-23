COURSE_DATA = {"course_name": "Algebra I", "course_id": "KA-ALG-01"}
STUDENT_DATA = {"student_name": "KA Student", "email": "kastudent@test.com"}
REPORT_DATA = {"student_id": "KA-STU-01", "report_type": "MONTHLY"}


class TestKaCourseCRUD:
    def test_create_course(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post("/ka/courses", json=COURSE_DATA, headers=auth_headers_admin)
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["course_name"] == COURSE_DATA["course_name"]
        assert "ka_course_code" in data

    def test_create_course_duplicate(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        client.post("/ka/courses", json=COURSE_DATA, headers=auth_headers_admin)
        resp = client.post("/ka/courses", json=COURSE_DATA, headers=auth_headers_admin)
        assert resp.status_code == 400

    def test_create_course_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/ka/courses", json=COURSE_DATA, headers=auth_headers_student
        )
        assert resp.status_code == 403

    def test_list_courses(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        client.post("/ka/courses", json=COURSE_DATA, headers=auth_headers_admin)
        resp = client.get("/ka/courses", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_course(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/ka/courses",
            json=COURSE_DATA,
            headers=auth_headers_admin,
        )
        course_id = create_resp.json()["ka_course_code"]
        resp = client.get(f"/ka/courses/{course_id}", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert resp.json()["course_name"] == COURSE_DATA["course_name"]

    def test_get_course_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/ka/courses/NONEXISTENT", headers=auth_headers_admin)
        assert resp.status_code == 404

    def test_update_course(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/ka/courses",
            json=COURSE_DATA,
            headers=auth_headers_admin,
        )
        course_id = create_resp.json()["ka_course_code"]
        resp = client.put(
            f"/ka/courses/{course_id}",
            json={"course_id": "KA-ALG-01", "course_name": "Algebra II"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200
        assert resp.json()["course_name"] == "Algebra II"

    def test_delete_course(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/ka/courses",
            json=COURSE_DATA,
            headers=auth_headers_admin,
        )
        course_id = create_resp.json()["ka_course_code"]
        resp = client.delete(f"/ka/courses/{course_id}", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    def test_delete_course_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.delete("/ka/courses/NONEXISTENT", headers=auth_headers_admin)
        assert resp.status_code == 404


class TestKaStudentCRUD:
    def test_create_student(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/ka/students",
            json=STUDENT_DATA,
            headers=auth_headers_admin,
        )
        assert resp.status_code == 201, resp.text
        assert resp.json()["student_name"] == STUDENT_DATA["student_name"]

    def test_list_students(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        client.post(
            "/ka/students",
            json=STUDENT_DATA,
            headers=auth_headers_admin,
        )
        resp = client.get("/ka/students", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_student(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/ka/students",
            json=STUDENT_DATA,
            headers=auth_headers_admin,
        )
        stu_id = create_resp.json()["ka_student_code"]
        resp = client.get(f"/ka/students/{stu_id}", headers=auth_headers_admin)
        assert resp.status_code == 200

    def test_delete_student(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/ka/students",
            json=STUDENT_DATA,
            headers=auth_headers_admin,
        )
        stu_id = create_resp.json()["ka_student_code"]
        resp = client.delete(f"/ka/students/{stu_id}", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert resp.json()["success"] is True


class TestKaReportCRUD:
    def test_create_report(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/ka/reports",
            json=REPORT_DATA,
            headers=auth_headers_admin,
        )
        assert resp.status_code == 201, resp.text
        assert "student_report_code" in resp.json()

    def test_list_reports(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        client.post("/ka/reports", json=REPORT_DATA, headers=auth_headers_admin)
        resp = client.get("/ka/reports", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_list_reports_filter_student(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        client.post("/ka/reports", json=REPORT_DATA, headers=auth_headers_admin)
        resp = client.get(
            "/ka/reports?student_id=KA-STU-01",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200

    def test_delete_report(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/ka/reports",
            json=REPORT_DATA,
            headers=auth_headers_admin,
        )
        report_id = create_resp.json()["student_report_code"]
        resp = client.delete(f"/ka/reports/{report_id}", headers=auth_headers_admin)
        assert resp.status_code == 200

    def test_report_unauthorized_create(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/ka/reports",
            json=REPORT_DATA,
            headers=auth_headers_student,
        )
        assert resp.status_code == 403
