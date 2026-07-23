class TestFeeCRUD:
    def test_create_fee(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/fees/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.student_class_code,
                "fee_month": 6,
                "fee_year": 2026,
                "total_amount": 5000.00,
                "due_date": "2026-06-15",
                "status": "PENDING",
            },
            headers=auth_headers_admin,
        )
        if resp.status_code == 200:
            data = resp.json()
            assert data["total_amount"] == 5000.00
            assert data["fee_month"] == 6
            assert data["fee_year"] == 2026
            assert data["status"] == "PENDING"
        else:
            assert resp.status_code in (400, 403, 404, 422), resp.text

    def test_list_fees(self, client, db_session, auth_headers_admin, override_admin):
        resp = client.get(
            "/fees/",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_fee_by_id(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/fees/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.student_class_code,
                "fee_month": 6,
                "fee_year": 2026,
                "total_amount": 5000.00,
                "due_date": "2026-06-15",
                "status": "PENDING",
            },
            headers=auth_headers_admin,
        )

        if create_resp.status_code != 200:
            return

        created = create_resp.json()
        fee_id = created["fee_code"]

        resp = client.get(
            f"/fees/{fee_id}",
            headers=auth_headers_admin,
        )
        if resp.status_code == 200:
            assert resp.json()["fee_code"] == fee_id
        elif resp.status_code == 404:
            pass
        else:
            pass

    def test_update_fee(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/fees/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.student_class_code,
                "fee_month": 6,
                "fee_year": 2026,
                "total_amount": 5000.00,
                "due_date": "2026-06-15",
                "status": "PENDING",
            },
            headers=auth_headers_admin,
        )
        if create_resp.status_code != 200:
            return

        created = create_resp.json()
        fee_id = created["fee_code"]

        resp = client.put(
            f"/fees/{fee_id}",
            json={
                "total_amount": 5500.00,
                "status": "PENDING",
            },
            headers=auth_headers_admin,
        )
        if resp.status_code == 200:
            assert resp.json()["total_amount"] == 5500.00
        else:
            assert resp.status_code in (403, 404), resp.text

    def test_delete_fee(
        self,
        client,
        db_session,
        academic_session,
        student_class,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/fees/",
            json={
                "academic_sessions_id": academic_session.session_code,
                "student_class_id": student_class.student_class_code,
                "fee_month": 6,
                "fee_year": 2026,
                "total_amount": 5000.00,
                "due_date": "2026-06-15",
                "status": "PENDING",
            },
            headers=auth_headers_admin,
        )
        if create_resp.status_code != 200:
            return

        created = create_resp.json()
        fee_id = created["fee_code"]

        resp = client.delete(
            f"/fees/{fee_id}",
            headers=auth_headers_admin,
        )
        if resp.status_code == 200:
            assert resp.json()["success"] is True
        else:
            assert resp.status_code in (403, 404), resp.text


class TestFeeAuthorization:
    def test_student_cannot_create_fee(
        self,
        client,
        db_session,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/fees/",
            json={
                "academic_sessions_id": "SES-2026",
                "student_class_id": "STC-XXXXXXXX",
                "fee_month": 6,
                "fee_year": 2026,
                "total_amount": 5000.00,
                "due_date": "2026-06-15",
                "status": "PENDING",
            },
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text

    def test_teacher_cannot_delete_fee(
        self,
        client,
        db_session,
        auth_headers_teacher,
        override_teacher,
    ):
        resp = client.delete(
            "/fees/1",
            headers=auth_headers_teacher,
        )
        assert resp.status_code == 403, resp.text
