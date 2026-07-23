import base64


def _b64_pdf():
    return base64.b64encode(b"%PDF-1.4 test content").decode()


UPLOAD_PAYLOAD = {
    "entity_type": "assignment",
    "entity_id": "ASN-001",
    "file_name": "test.pdf",
    "mime_type": "application/pdf",
    "file_data": _b64_pdf(),
}


class TestAttachmentCRUD:
    def test_upload_attachment(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/attachments/upload",
            json=UPLOAD_PAYLOAD,
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True
        assert "attachment_id" in data

    def test_upload_attachment_missing_fields(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/attachments/upload",
            json={"entity_type": "assignment"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 400, resp.text

    def test_upload_attachment_invalid_mime(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        payload = {**UPLOAD_PAYLOAD, "mime_type": "application/exe"}
        resp = client.post(
            "/attachments/upload",
            json=payload,
            headers=auth_headers_admin,
        )
        assert resp.status_code == 400, resp.text

    def test_download_attachment(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/attachments/upload",
            json=UPLOAD_PAYLOAD,
            headers=auth_headers_admin,
        )
        att_id = create_resp.json()["attachment_id"]
        resp = client.get(f"/attachments/{att_id}", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.headers["Content-Type"] == "application/pdf"

    def test_download_attachment_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/attachments/99999", headers=auth_headers_admin)
        assert resp.status_code == 404

    def test_list_entity_attachments(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        client.post(
            "/attachments/upload",
            json=UPLOAD_PAYLOAD,
            headers=auth_headers_admin,
        )
        resp = client.get(
            "/attachments/entity/assignment/ASN-001",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True
        assert len(data["data"]) >= 1

    def test_update_attachment(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/attachments/upload",
            json=UPLOAD_PAYLOAD,
            headers=auth_headers_admin,
        )
        att_id = create_resp.json()["attachment_id"]
        resp = client.put(
            f"/attachments/{att_id}",
            json={"file_name": "renamed.pdf"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["file_name"] == "renamed.pdf"

    def test_update_attachment_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.put(
            "/attachments/99999",
            json={"file_name": "test.pdf"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 404

    def test_delete_attachment(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/attachments/upload",
            json=UPLOAD_PAYLOAD,
            headers=auth_headers_admin,
        )
        att_id = create_resp.json()["attachment_id"]
        resp = client.delete(f"/attachments/{att_id}", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True

    def test_delete_attachment_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.delete("/attachments/99999", headers=auth_headers_admin)
        assert resp.status_code == 404

    def test_delete_attachment_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.delete("/attachments/NONEXISTENT", headers=auth_headers_student)
        assert resp.status_code == 404
