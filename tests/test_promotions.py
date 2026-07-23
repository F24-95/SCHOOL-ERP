from datetime import date

import pytest


@pytest.fixture
def from_academic_session(db_session, admin_user):
    from app.model import AcademicSession

    obj = AcademicSession(
        session_code="SES-2025",
        session_name="2025-26",
        start_year=2025,
        end_year=2026,
        start_date=date(2025, 4, 1),
        end_date=date(2026, 3, 31),
        is_current=False,
        created_by=admin_user.user_code,
    )
    db_session.add(obj)
    db_session.flush()
    return obj


@pytest.fixture
def from_classroom(db_session, from_academic_session, admin_user):
    from app.model import ClassRoom

    cls = ClassRoom(
        class_code="CLS9A",
        class_name="Class 9",
        section="A",
        display_name="Class 9-A",
        academic_sessions_id=from_academic_session.session_code,
        created_by=admin_user.user_code,
    )
    db_session.add(cls)
    db_session.flush()
    return cls


@pytest.fixture
def promotion_student(student_user):
    return student_user


class TestPromotionCRUD:
    def test_create_promotion(
        self,
        client,
        db_session,
        seed_all,
        from_classroom,
        classroom,
        academic_session,
        student_user,
        auth_headers_admin,
        override_admin,
    ):
        data = {
            "student_id": student_user.student_profile.student_id,
            "from_session_id": "SES-2025",
            "to_session_id": academic_session.session_code,
            "from_classroom_id": from_classroom.class_code,
            "to_classroom_id": classroom.class_code,
            "previous_roll_number": 10,
            "new_roll_number": 5,
        }
        resp = client.post(
            "/promotions",
            json=data,
            headers=auth_headers_admin,
        )
        assert resp.status_code == 201, resp.text
        assert resp.json()["student_id"] == student_user.student_profile.student_id

    def test_create_promotion_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/promotions",
            json={
                "student_id": "x",
                "from_session_id": "x",
                "to_session_id": "x",
                "from_classroom_id": "x",
                "to_classroom_id": "x",
                "previous_roll_number": 1,
                "new_roll_number": 1,
            },
            headers=auth_headers_student,
        )
        assert resp.status_code == 403

    def test_list_promotions(
        self,
        client,
        db_session,
        seed_all,
        from_classroom,
        classroom,
        academic_session,
        student_user,
        auth_headers_admin,
        override_admin,
    ):
        data = {
            "student_id": student_user.student_profile.student_id,
            "from_session_id": "SES-2025",
            "to_session_id": academic_session.session_code,
            "from_classroom_id": from_classroom.class_code,
            "to_classroom_id": classroom.class_code,
            "previous_roll_number": 10,
            "new_roll_number": 5,
        }
        client.post("/promotions", json=data, headers=auth_headers_admin)
        resp = client.get("/promotions", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert isinstance(resp.json(), list)

    def test_get_promotion(
        self,
        client,
        db_session,
        seed_all,
        from_classroom,
        classroom,
        academic_session,
        student_user,
        auth_headers_admin,
        override_admin,
    ):
        data = {
            "student_id": student_user.student_profile.student_id,
            "from_session_id": "SES-2025",
            "to_session_id": academic_session.session_code,
            "from_classroom_id": from_classroom.class_code,
            "to_classroom_id": classroom.class_code,
            "previous_roll_number": 10,
            "new_roll_number": 5,
        }
        create_resp = client.post("/promotions", json=data, headers=auth_headers_admin)
        prom_id = create_resp.json()["promotion_history_code"]
        resp = client.get(f"/promotions/{prom_id}", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["promotion_history_code"] == prom_id

    def test_get_promotion_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/promotions/NONEXISTENT", headers=auth_headers_admin)
        assert resp.status_code == 404

    def test_update_promotion(
        self,
        client,
        db_session,
        seed_all,
        from_classroom,
        classroom,
        academic_session,
        student_user,
        auth_headers_admin,
        override_admin,
    ):
        data = {
            "student_id": student_user.student_profile.student_id,
            "from_session_id": "SES-2025",
            "to_session_id": academic_session.session_code,
            "from_classroom_id": from_classroom.class_code,
            "to_classroom_id": classroom.class_code,
            "previous_roll_number": 10,
            "new_roll_number": 5,
        }
        create_resp = client.post("/promotions", json=data, headers=auth_headers_admin)
        prom_id = create_resp.json()["promotion_history_code"]
        resp = client.put(
            f"/promotions/{prom_id}",
            json={"remarks": "Updated remarks", "new_roll_number": 6},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["new_roll_number"] == 6

    def test_update_promotion_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.put(
            "/promotions/NONEXISTENT",
            json={"remarks": "test"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 404

    def test_delete_promotion(
        self,
        client,
        db_session,
        seed_all,
        from_classroom,
        classroom,
        academic_session,
        student_user,
        auth_headers_admin,
        override_admin,
    ):
        data = {
            "student_id": student_user.student_profile.student_id,
            "from_session_id": "SES-2025",
            "to_session_id": academic_session.session_code,
            "from_classroom_id": from_classroom.class_code,
            "to_classroom_id": classroom.class_code,
            "previous_roll_number": 10,
            "new_roll_number": 5,
        }
        create_resp = client.post("/promotions", json=data, headers=auth_headers_admin)
        prom_id = create_resp.json()["promotion_history_code"]
        resp = client.delete(f"/promotions/{prom_id}", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True

    def test_delete_promotion_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.delete("/promotions/NONEXISTENT", headers=auth_headers_admin)
        assert resp.status_code == 404

    def test_promotion_unauthorized_list(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.get("/promotions", headers=auth_headers_student)
        assert resp.status_code == 403
