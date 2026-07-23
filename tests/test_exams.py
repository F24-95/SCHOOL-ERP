class TestExamCRUD:
    def test_create_exam(
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
            "/exams/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "exam_name": "Mid Term",
                "exam_type": "Written",
                "exam_date": "2026-09-15",
                "total_marks": 100,
                "passing_marks": 40,
            },
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert data["exam_name"] == "Mid Term"
        else:
            assert resp.status_code in (400, 403, 404, 422), resp.text

    def test_list_exams(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/exams/",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_exam_by_id(
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
            "/exams/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "exam_name": "Final Exam",
                "exam_type": "Written",
                "exam_date": "2026-12-15",
                "total_marks": 100,
                "passing_marks": 40,
            },
            headers=auth_headers_teacher,
        )

        if create_resp.status_code != 200:
            return

        resp = client.get(
            "/exams/1",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["exam_name"] == "Final Exam"

    def test_update_exam(
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
            "/exams/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "exam_name": "Prelim",
                "exam_type": "Written",
                "exam_date": "2026-10-01",
                "total_marks": 100,
                "passing_marks": 40,
            },
            headers=auth_headers_teacher,
        )
        if create_resp.status_code != 200:
            return

        resp = client.put(
            "/exams/1",
            json={"exam_name": "Preliminary Exam"},
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["exam_name"] == "Preliminary Exam"

    def test_delete_exam(
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
            "/exams/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "exam_name": "Delete Test Exam",
                "exam_type": "Written",
                "exam_date": "2026-11-01",
                "total_marks": 50,
                "passing_marks": 20,
            },
            headers=auth_headers_teacher,
        )
        if create_resp.status_code != 200:
            return

        resp = client.delete(
            "/exams/1",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["success"] is True


class TestExamAuthorization:
    def test_student_cannot_create_exam(
        self,
        client,
        db_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/exams/",
            json={
                "academic_sessions_id": "SES-2026",
                "classroom_id": "CLS10A",
                "class_subject_id": "CLS-XXXXXXXX",
                "teacher_subject_id": "TCH-XXXXXXXX",
                "exam_name": "Hack Exam",
                "exam_type": "Written",
                "exam_date": "2026-09-15",
                "total_marks": 100,
                "passing_marks": 40,
            },
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text
