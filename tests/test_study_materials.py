MATERIAL_DATA = {
    "academic_sessions_id": "SES-2026",
    "classroom_id": "CLS10A",
    "title": "Math Chapter 1",
    "description": "Introduction to Algebra",
    "material_type": "PDF",
}


class TestStudyMaterialCRUD:
    def test_create_material(
        self,
        client,
        db_session,
        seed_all,
        class_subject,
        teacher_subject,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.post(
            "/study-materials/",
            data={
                **MATERIAL_DATA,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
            },
            files={"file": ("test.pdf", b"%PDF-1.4 test content", "application/pdf")},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["title"] == MATERIAL_DATA["title"]
        assert data["description"] == MATERIAL_DATA["description"]
        assert "material_code" in data

    def test_list_materials(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/study-materials/", headers=auth_headers_admin)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list)

    def test_get_material(
        self,
        client,
        db_session,
        seed_all,
        class_subject,
        teacher_subject,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/study-materials/",
            data={
                **MATERIAL_DATA,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
            },
            files={"file": ("test.pdf", b"%PDF-1.4 test content", "application/pdf")},
            headers=auth_headers_admin,
        )
        assert create_resp.status_code == 200, create_resp.text
        material_id = create_resp.json()["material_code"]

        resp = client.get(
            f"/study-materials/{material_id}",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["title"] == MATERIAL_DATA["title"]

    def test_delete_material(
        self,
        client,
        db_session,
        seed_all,
        class_subject,
        teacher_subject,
        auth_headers_admin,
        override_admin,
    ):
        create_resp = client.post(
            "/study-materials/",
            data={
                **MATERIAL_DATA,
                "class_subject_id": class_subject.class_subject_code,
                "teacher_subject_id": teacher_subject.teacher_subject_code,
            },
            files={"file": ("test.pdf", b"%PDF-1.4 test content", "application/pdf")},
            headers=auth_headers_admin,
        )
        assert create_resp.status_code == 200, create_resp.text
        material_id = create_resp.json()["material_code"]

        resp = client.delete(
            f"/study-materials/{material_id}",
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["success"] is True


class TestStudyMaterialAuthorization:
    def test_student_cannot_create_material(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.post(
            "/study-materials/",
            data={
                **MATERIAL_DATA,
                "class_subject_id": "CS-123",
                "teacher_subject_id": "TS-123",
            },
            files={"file": ("test.pdf", b"%PDF-1.4 test content", "application/pdf")},
            headers=auth_headers_student,
        )
        assert resp.status_code == 403, resp.text
