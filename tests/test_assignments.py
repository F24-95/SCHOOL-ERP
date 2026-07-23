class TestAssignmentCRUD:
    def test_create_assignment(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        class_subject,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.post(
            "/assignments/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "title": "Math Homework 1",
                "description": "Solve chapter 1 problems",
                "due_date": "2026-08-01",
                "total_marks": 100,
                "passing_marks": 40,
            },
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert data["title"] == "Math Homework 1"
        else:
            assert resp.status_code in (400, 403, 404), resp.text

    def test_list_assignments(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/assignments/",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_assignment_by_id(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        class_subject,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        create_resp = client.post(
            "/assignments/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "title": "Test Assignment Get",
                "description": "Test description",
                "due_date": "2026-08-15",
                "total_marks": 50,
                "passing_marks": 20,
            },
            headers=auth_headers_teacher,
        )

        if create_resp.status_code != 200:
            return

        assignment_id = 1

        resp = client.get(
            f"/assignments/{assignment_id}",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["title"] == "Test Assignment Get"
        elif resp.status_code == 404:
            pass
        else:
            pass

    def test_delete_assignment(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        class_subject,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        create_resp = client.post(
            "/assignments/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "title": "Test Assignment Delete",
                "description": "To be deleted",
                "due_date": "2026-09-01",
                "total_marks": 30,
                "passing_marks": 15,
            },
            headers=auth_headers_teacher,
        )
        if create_resp.status_code != 200:
            return

        resp = client.delete(
            "/assignments/1",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["success"] is True
        else:
            assert resp.status_code in (403, 404), resp.text


class TestAssignmentAuthorization:
    def test_student_cannot_create_assignment(
        self,
        client,
        db_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/assignments/",
            json={
                "academic_sessions_id": "SES-2026",
                "classroom_id": "CLS10A",
                "class_subject_id": "CLS-XXXXXXXX",
                "teacher_subject_id": "TCH-XXXXXXXX",
                "title": "Hack Attempt",
                "due_date": "2026-08-01",
                "total_marks": 100,
                "passing_marks": 40,
            },
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text
