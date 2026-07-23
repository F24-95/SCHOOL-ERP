NOTICE_DATA = {
    "academic_sessions_id": "SES-2026",
    "title": "School Holiday",
    "description": "School will remain closed on Friday",
    "notice_type": "GENERAL",
    "audience": "ALL",
    "publish_date": "2026-07-21",
}


class TestNoticeCRUD:
    def test_create_notice(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        resp = client.post("/notices/", data=NOTICE_DATA, headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["title"] == NOTICE_DATA["title"]
        assert data["description"] == NOTICE_DATA["description"]
        assert "notice_code" in data

    def test_list_notices(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        client.post("/notices/", data=NOTICE_DATA, headers=auth_headers_admin)
        resp = client.get("/notices/", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_notice(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        create_resp = client.post(
            "/notices/", data=NOTICE_DATA, headers=auth_headers_admin
        )
        assert create_resp.status_code == 200, create_resp.text
        notice_id = create_resp.json()["notice_code"]

        resp = client.get(f"/notices/{notice_id}", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["title"] == NOTICE_DATA["title"]

    def test_update_notice(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        create_resp = client.post(
            "/notices/", data=NOTICE_DATA, headers=auth_headers_admin
        )
        assert create_resp.status_code == 200, create_resp.text
        notice_id = create_resp.json()["notice_code"]

        resp = client.put(
            f"/notices/{notice_id}",
            data={"title": "Updated Title"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["title"] == "Updated Title"

    def test_delete_notice(
        self, client, db_session, seed_all, auth_headers_admin, override_admin
    ):
        create_resp = client.post(
            "/notices/", data=NOTICE_DATA, headers=auth_headers_admin
        )
        assert create_resp.status_code == 200, create_resp.text
        notice_id = create_resp.json()["notice_code"]

        resp = client.delete(f"/notices/{notice_id}", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True


class TestNoticeAuthorization:
    def test_student_cannot_create_notice(
        self, client, db_session, seed_all, auth_headers_student, override_student
    ):
        resp = client.post("/notices/", data=NOTICE_DATA, headers=auth_headers_student)
        assert resp.status_code == 403, resp.text
