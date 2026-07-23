import pytest


@pytest.fixture
def ka_course(db_session):
    from app.helpers.code_generators import generate_ka_course_id
    from app.model import KaCourse

    c = KaCourse(
        business_id=generate_ka_course_id(),
        course_name="Test Course",
        course_id="COURSE-001",
    )
    db_session.add(c)
    db_session.flush()
    return c


TOPIC_DATA = {"topic_id": "TOP-001", "topic_name": "Linear Equations"}
PROGRESS_DATA = {
    "student_id": "STU-001",
    "topic_id": "TOP-001",
    "point_available": 10,
    "point_earned": 8,
}


class TestTopicCRUD:
    def test_create_topic(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        resp = client.post("/topics", json=data, headers=auth_headers_admin)
        assert resp.status_code == 201, resp.text
        assert resp.json()["topic_name"] == TOPIC_DATA["topic_name"]
        assert "business_id" in resp.json()

    def test_create_topic_duplicate(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        client.post("/topics", json=data, headers=auth_headers_admin)
        resp = client.post("/topics", json=data, headers=auth_headers_admin)
        assert resp.status_code == 400

    def test_create_topic_unauthorized(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.post("/topics", json=TOPIC_DATA, headers=auth_headers_student)
        assert resp.status_code == 403

    def test_list_topics(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        client.post("/topics", json=data, headers=auth_headers_admin)
        resp = client.get("/topics", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_list_topics_filter_course(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        client.post("/topics", json=data, headers=auth_headers_admin)
        resp = client.get(
            "/topics?course_id=" + ka_course.business_id, headers=auth_headers_admin
        )
        assert resp.status_code == 200

    def test_get_topic(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        create_resp = client.post("/topics", json=data, headers=auth_headers_admin)
        topic_id = create_resp.json()["business_id"]
        resp = client.get(f"/topics/{topic_id}", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert resp.json()["topic_name"] == TOPIC_DATA["topic_name"]

    def test_get_topic_not_found(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/topics/NONEXISTENT", headers=auth_headers_admin)
        assert resp.status_code == 404

    def test_update_topic(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        create_resp = client.post("/topics", json=data, headers=auth_headers_admin)
        topic_id = create_resp.json()["business_id"]
        resp = client.put(
            f"/topics/{topic_id}",
            json={"topic_id": "TOP-001", "topic_name": "Quadratic Equations"},
            headers=auth_headers_admin,
        )
        assert resp.status_code == 200
        assert resp.json()["topic_name"] == "Quadratic Equations"

    def test_delete_topic(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_admin,
        override_admin,
    ):
        data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        create_resp = client.post("/topics", json=data, headers=auth_headers_admin)
        topic_id = create_resp.json()["business_id"]
        resp = client.delete(f"/topics/{topic_id}", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert resp.json()["success"] is True


@pytest.fixture
def ka_student(db_session):
    from app.helpers.code_generators import generate_ka_student_id
    from app.model import KaStudent

    s = KaStudent(
        business_id=generate_ka_student_id(),
        student_name="Progress Student",
        email="progress@test.com",
    )
    db_session.add(s)
    db_session.flush()
    return s


class TestTopicProgressCRUD:
    def test_create_topic_progress(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        ka_student,
        auth_headers_admin,
        override_admin,
    ):
        topic_data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        topic_resp = client.post("/topics", json=topic_data, headers=auth_headers_admin)
        topic_biz_id = topic_resp.json()["business_id"]
        data = {
            "student_id": ka_student.business_id,
            "topic_id": topic_biz_id,
            "point_available": 10,
            "point_earned": 8,
        }
        resp = client.post("/topics/progress", json=data, headers=auth_headers_admin)
        assert resp.status_code == 201, resp.text
        assert "business_id" in resp.json()

    def test_list_topic_progress(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_admin,
        override_admin,
    ):
        resp = client.get("/topics/progress", headers=auth_headers_admin)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_topic_progress(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        ka_student,
        auth_headers_admin,
        override_admin,
    ):
        topic_data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        topic_resp = client.post("/topics", json=topic_data, headers=auth_headers_admin)
        topic_biz_id = topic_resp.json()["business_id"]
        create = client.post(
            "/topics/progress",
            json={
                "student_id": ka_student.business_id,
                "topic_id": topic_biz_id,
                "point_available": 10,
                "point_earned": 8,
            },
            headers=auth_headers_admin,
        )
        tp_id = create.json()["business_id"]
        resp = client.get(f"/topics/progress/{tp_id}", headers=auth_headers_admin)
        assert resp.status_code == 200

    def test_delete_topic_progress(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        ka_student,
        auth_headers_admin,
        override_admin,
    ):
        topic_data = {**TOPIC_DATA, "course_id": ka_course.business_id}
        topic_resp = client.post("/topics", json=topic_data, headers=auth_headers_admin)
        topic_biz_id = topic_resp.json()["business_id"]
        create = client.post(
            "/topics/progress",
            json={
                "student_id": ka_student.business_id,
                "topic_id": topic_biz_id,
                "point_available": 10,
                "point_earned": 8,
            },
            headers=auth_headers_admin,
        )
        tp_id = create.json()["business_id"]
        resp = client.delete(f"/topics/progress/{tp_id}", headers=auth_headers_admin)
        assert resp.status_code == 200


class TestTopicAuthorization:
    def test_student_cannot_create_topic(
        self,
        client,
        db_session,
        seed_all,
        auth_headers_student,
        override_student,
    ):
        resp = client.post("/topics", json=TOPIC_DATA, headers=auth_headers_student)
        assert resp.status_code == 403

    def test_teacher_cannot_delete_topic(
        self,
        client,
        db_session,
        seed_all,
        ka_course,
        auth_headers_teacher,
        override_teacher,
    ):
        from app.helpers.code_generators import generate_topic_id
        from app.model.topic import Topic

        topic = Topic(
            business_id=generate_topic_id(),
            topic_id="AUTH-TOPIC-ID",
            topic_name="Topic for auth test",
            course_id=ka_course.business_id,
        )
        db_session.add(topic)
        db_session.flush()
        resp = client.delete(
            f"/topics/{topic.business_id}", headers=auth_headers_teacher
        )
        assert resp.status_code == 403
