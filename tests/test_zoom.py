class TestZoomMeetingCRUD:
    def test_create_meeting(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/zoom/meetings",
            json={
                "uuid": "zoom-uuid-001",
                "meeting_id": "123456789",
                "topic": "Math Class Review",
                "type": 2,
                "start_time": "2026-07-21T10:00:00",
                "duration": 60,
                "timezone": "Asia/Kolkata",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["uuid"] == "zoom-uuid-001"
        assert data["topic"] == "Math Class Review"
        assert data["duration"] == 60

    def test_create_duplicate_meeting(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-dup", "topic": "First"},
            headers=auth_headers_admin,
        )
        resp = client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-dup", "topic": "Duplicate"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 400, resp.text

    def test_list_meetings(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-list-1", "topic": "Meeting A"},
            headers=auth_headers_admin,
        )
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-list-2", "topic": "Meeting B"},
            headers=auth_headers_admin,
        )
        resp = client.get("/zoom/meetings", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert len(data) >= 2

    def test_list_meetings_filter_host(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        client.post(
            "/zoom/meetings",
            json={
                "uuid": "zoom-uuid-host-1",
                "host_id": "hostA",
                "topic": "Host A Meeting",
            },
            headers=auth_headers_admin,
        )
        resp = client.get("/zoom/meetings?host_id=hostA", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        for m in resp.json():
            assert m["host_id"] == "hostA"

    def test_get_meeting(self, client, db_session, auth_headers_admin, override_admin):
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-get", "topic": "Get Me"},
            headers=auth_headers_admin,
        )
        resp = client.get("/zoom/meetings/zoom-uuid-get", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["uuid"] == "zoom-uuid-get"

    def test_get_meeting_not_found(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get(
            "/zoom/meetings/non-existent-uuid", headers=auth_headers_admin
        )
        assert resp.status_code == 404, resp.text

    def test_update_meeting(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-upd", "topic": "Old Topic", "duration": 30},
            headers=auth_headers_admin,
        )
        resp = client.put(
            "/zoom/meetings/zoom-uuid-upd",
            json={"topic": "Updated Topic", "duration": 45},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["topic"] == "Updated Topic"
        assert data["duration"] == 45

    def test_delete_meeting(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-del", "topic": "Delete Me"},
            headers=auth_headers_admin,
        )
        resp = client.delete("/zoom/meetings/zoom-uuid-del", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True
        get_resp = client.get(
            "/zoom/meetings/zoom-uuid-del", headers=auth_headers_admin
        )
        assert get_resp.status_code == 404

    def test_delete_meeting_not_found(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.delete("/zoom/meetings/no-such-uuid", headers=auth_headers_admin)
        assert resp.status_code == 404, resp.text

    def test_meeting_unauthorized(
        self, client, db_session, auth_headers_student, override_student
    ):
        resp = client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-uuid-auth", "topic": "Hack"},
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text


class TestZoomRecordingFileCRUD:
    def setup_meeting(self, client, auth_headers_admin):
        client.post(
            "/zoom/meetings",
            json={"uuid": "zoom-rec-meeting", "topic": "Recording Test Meeting"},
            headers=auth_headers_admin,
        )

    def test_create_recording(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        resp = client.post(
            "/zoom/recordings",
            json={
                "id": "rec-001",
                "meeting_uuid": "zoom-rec-meeting",
                "file_type": "MP4",
                "file_size": 1048576,
                "status": "completed",
                "recording_type": "shared_screen_with_speaker_view",
            },
            headers=auth_headers_admin,
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["id"] == "rec-001"
        assert data["meeting_uuid"] == "zoom-rec-meeting"

    def test_create_recording_duplicate(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        client.post(
            "/zoom/recordings",
            json={"id": "rec-dup", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        resp = client.post(
            "/zoom/recordings",
            json={"id": "rec-dup", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 400, resp.text

    def test_create_recording_missing_meeting(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.post(
            "/zoom/recordings",
            json={"id": "rec-no-meeting", "meeting_uuid": "non-existent-meeting"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 404, resp.text

    def test_list_recordings(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        client.post(
            "/zoom/recordings",
            json={"id": "rec-list-1", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        client.post(
            "/zoom/recordings",
            json={"id": "rec-list-2", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        resp = client.get("/zoom/recordings", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert len(resp.json()) >= 2

    def test_list_recordings_filter_meeting(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        client.post(
            "/zoom/recordings",
            json={"id": "rec-filter", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        resp = client.get(
            "/zoom/recordings?meeting_uuid=zoom-rec-meeting",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        for r in resp.json():
            assert r["meeting_uuid"] == "zoom-rec-meeting"

    def test_get_recording(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        client.post(
            "/zoom/recordings",
            json={"id": "rec-get", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        resp = client.get("/zoom/recordings/rec-get", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["id"] == "rec-get"

    def test_get_recording_not_found(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.get("/zoom/recordings/no-such-rec", headers=auth_headers_admin)
        assert resp.status_code == 404, resp.text

    def test_update_recording(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        client.post(
            "/zoom/recordings",
            json={
                "id": "rec-upd",
                "meeting_uuid": "zoom-rec-meeting",
                "status": "processing",
            },
            headers=auth_headers_admin,
        )
        resp = client.put(
            "/zoom/recordings/rec-upd",
            json={"status": "completed"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["status"] == "completed"

    def test_delete_recording(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        self.setup_meeting(client, auth_headers_admin)
        client.post(
            "/zoom/recordings",
            json={"id": "rec-del", "meeting_uuid": "zoom-rec-meeting"},
            headers=auth_headers_admin,
        )
        resp = client.delete("/zoom/recordings/rec-del", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True
        get_resp = client.get("/zoom/recordings/rec-del", headers=auth_headers_admin)
        assert get_resp.status_code == 404

    def test_delete_recording_not_found(
        self, client, db_session, auth_headers_admin, override_admin
    ):
        resp = client.delete("/zoom/recordings/no-such-rec", headers=auth_headers_admin)
        assert resp.status_code == 404, resp.text

    def test_recording_unauthorized(
        self, client, db_session, auth_headers_teacher, override_teacher
    ):
        resp = client.post(
            "/zoom/recordings",
            json={"id": "rec-auth", "meeting_uuid": "some-meeting"},
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 403, resp.text
