class TestSubjectCRUD:
    def test_create_subject(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/subjects/",
            json={
                "subject_code": "CHEM10",
                "subject_name": "Chemistry",
                "subject_type": "Core",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["subject_code"] == "CHEM10"

    def test_create_duplicate_subject_code(
        self, client, db_session, subject, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/subjects/",
            json={
                "subject_code": "MATH10",
                "subject_name": "Mathematics Advanced",
                "subject_type": "Core",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 400, resp.text

    def test_list_subjects(
        self, client, db_session, subject, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/subjects/",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert len(data) >= 1

    def test_get_subject(
        self, client, db_session, subject, auth_headers_admin, override_admin
    ):
        resp = client.get(
            f"/subjects/{subject.subject_code}",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["subject_code"] == subject.subject_code

    def test_get_nonexistent_subject(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/subjects/INVALID99",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 404, resp.text

    def test_update_subject(
        self, client, db_session, subject, auth_headers_admin, override_admin
    ):
        resp = client.put(
            f"/subjects/{subject.subject_code}",
            json={"subject_name": "Advanced Mathematics"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["subject_name"] == "Advanced Mathematics"

    def test_soft_delete_subject(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/subjects/",
            json={
                "subject_code": "TEMP01",
                "subject_name": "Temporary Subject",
                "subject_type": "Elective",
            },
            headers=auth_headers_admin,
        )
        subj_code = resp.json()["subject_code"]

        resp = client.delete(
            f"/subjects/{subj_code}",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True


class TestClassSubjectMapping:
    def test_assign_subject_to_class(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        subject,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/subjects/class-subjects",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "subject_id": subject.subject_code,
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "business_id" in data

    def test_assign_duplicate_class_subject(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        subject,
        class_subject,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/subjects/class-subjects",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "subject_id": subject.subject_code,
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code in (400, 409), resp.text

    def test_list_class_subjects(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/subjects/class-subjects",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text

    def test_get_subjects_for_class(
        self,
        client,
        db_session,
        classroom,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get(
            f"/subjects/classes/{classroom.class_code}/subjects",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text


class TestSubjectAuthorization:
    def test_student_cannot_create_subject(
        self,
        client,
        db_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/subjects/",
            json={
                "subject_code": "BIO10",
                "subject_name": "Biology",
                "subject_type": "Core",
            },
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text

    def test_teacher_cannot_create_subject(
        self,
        client,
        db_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.post(
            "/subjects/",
            json={
                "subject_code": "BIO10",
                "subject_name": "Biology",
                "subject_type": "Core",
            },
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 403, resp.text
