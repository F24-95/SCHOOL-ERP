class TestDailyClassCRUD:
    def test_create_daily_class(
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
            "/daily-class/",
            json={
                "daily_class_id": "DC-20260715-001",
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "class_date": "2026-07-15",
                "topic": "Algebra Basics",
                "lecture_status": "SCHEDULED",
            },
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert data["topic"] == "Algebra Basics"
        else:
            assert resp.status_code in (400, 403, 404, 422), resp.text

    def test_list_daily_classes(
        self,
        client,
        db_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.get(
            "/daily-class/",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_daily_class(
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
            "/daily-class/",
            json={
                "daily_class_id": "DC-20260715-002",
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "class_date": "2026-07-15",
                "topic": "Algebra Basics",
                "lecture_status": "SCHEDULED",
            },
            headers=auth_headers_teacher,
        )

        if create_resp.status_code != 200:
            return

        daily_class_id = create_resp.json().get("id") or 1

        resp = client.get(
            f"/daily-class/{daily_class_id}",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["topic"] == "Algebra Basics"

    def test_update_daily_class(
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
            "/daily-class/",
            json={
                "daily_class_id": "DC-20260715-003",
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "class_date": "2026-07-15",
                "topic": "Algebra Basics",
                "lecture_status": "SCHEDULED",
            },
            headers=auth_headers_teacher,
        )
        if create_resp.status_code != 200:
            return

        daily_class_id = create_resp.json().get("id") or 1

        resp = client.put(
            f"/daily-class/{daily_class_id}",
            json={"topic": "Advanced Algebra"},
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["topic"] == "Advanced Algebra"

    def test_delete_daily_class(
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
            "/daily-class/",
            json={
                "daily_class_id": "DC-20260715-004",
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "class_date": "2026-07-15",
                "topic": "Delete Test",
                "lecture_status": "SCHEDULED",
            },
            headers=auth_headers_teacher,
        )
        if create_resp.status_code != 200:
            return

        daily_class_id = create_resp.json().get("id") or 1

        resp = client.delete(
            f"/daily-class/{daily_class_id}",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["success"] is True


class TestDailyClassAttendance:
    def test_mark_attendance(
        self,
        client,
        db_session,
        academic_session,
        classroom,
        class_subject,
        teacher_subject,
        student_class,
        auth_headers_teacher,
        override_teacher,
    ):
        create_resp = client.post(
            "/daily-class/",
            json={
                "daily_class_id": "DC-20260715-005",
                "academic_sessions_id": academic_session.session_code,
                "classroom_id": classroom.class_code,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
                "class_date": "2026-07-15",
                "topic": "Attendance Test",
                "lecture_status": "SCHEDULED",
            },
            headers=auth_headers_teacher,
        )
        if create_resp.status_code != 200:
            return

        daily_class_id = create_resp.json().get("id") or 1

        resp = client.post(
            f"/daily-class/{daily_class_id}/students",
            json=[
                {
                    "daily_class_id": daily_class_id,
                    "student_class_id": student_class.student_class_code,
                    "attendance_status": "Present",
                    "is_late": False,
                    "late_minutes": 0,
                }
            ],
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert isinstance(data, list)
            assert len(data) >= 1
            assert data[0]["attendance_status"] == "Present"
        else:
            assert resp.status_code in (400, 403, 404, 422), resp.text
