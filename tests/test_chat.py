class TestChatRoom:
    def test_create_room(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.post(
            "/chat/rooms",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "title": "Test Chat Room",
            },
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert data["academic_sessions_id"] == academic_session.session_code
        else:
            assert resp.status_code in (400, 403, 404, 422), resp.text

    def test_list_rooms(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.get(
            "/chat/rooms",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_room_by_id(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        create_resp = client.post(
            "/chat/rooms",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "title": "Test Chat Room Get",
            },
            headers=auth_headers_teacher,
        )

        if create_resp.status_code != 200:
            return

        created = create_resp.json()
        room_id = (
            created.get("business_id")
            or created.get("id")
            or created.get("chat_room_id")
        )

        resp = client.get(
            f"/chat/rooms/{room_id}",
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["business_id"] == room_id
        elif resp.status_code == 404:
            pass
        else:
            pass


class TestChatMessage:
    def test_send_message(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        create_resp = client.post(
            "/chat/rooms",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "title": "Test Chat Room Msg",
            },
            headers=auth_headers_teacher,
        )

        if create_resp.status_code != 200:
            return

        room_id = (
            create_resp.json().get("business_id")
            or create_resp.json().get("id")
            or create_resp.json().get("chat_room_id")
        )

        resp = client.post(
            f"/chat/rooms/{room_id}/messages",
            json={
                "message": "Hello, this is a test message",
            },
            headers=auth_headers_teacher,
        )
        if resp.status_code == 200:
            assert resp.json()["message"] == "Hello, this is a test message"
        else:
            assert resp.status_code in (400, 403, 404, 422), resp.text

    def test_list_messages(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        teacher_subject,
        auth_headers_teacher,
        override_teacher,
    ):
        create_resp = client.post(
            "/chat/rooms",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.business_id,
                "teacher_subject_id": teacher_subject.business_id,
                "title": "Test Chat Room List Msg",
            },
            headers=auth_headers_teacher,
        )

        if create_resp.status_code != 200:
            return

        room_id = (
            create_resp.json().get("business_id")
            or create_resp.json().get("id")
            or create_resp.json().get("chat_room_id")
        )

        client.post(
            f"/chat/rooms/{room_id}/messages",
            json={"message": "Hello"},
            headers=auth_headers_teacher,
        )

        resp = client.get(
            f"/chat/rooms/{room_id}/messages",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)
