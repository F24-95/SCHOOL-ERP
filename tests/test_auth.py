class TestHealth:
    def test_health_endpoint(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "authentication"
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "running"


class TestLogin:
    def test_login_success_admin(self, client, db_session, admin_user):
        resp = client.post(
            "/login",
            json={"email": "admin@test.edu", "password": "admin@123"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "admin@test.edu"

    def test_login_success_teacher(self, client, db_session, teacher_user):
        resp = client.post(
            "/login",
            json={"email": "teacher@test.edu", "password": "teacher@123"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "access_token" in data

    def test_login_success_student(self, client, db_session, student_user):
        resp = client.post(
            "/login",
            json={"email": "student@test.edu", "password": "student@123"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "access_token" in data

    def test_login_invalid_password(self, client, db_session, admin_user):
        resp = client.post(
            "/login",
            json={"email": "admin@test.edu", "password": "wrongpassword"},
        )
        assert resp.status_code == 401, resp.text

    def test_login_nonexistent_user(self, client):
        resp = client.post(
            "/login",
            json={"email": "nobody@test.com", "password": "password123"},
        )
        assert resp.status_code == 401, resp.text

    def test_login_oauth2(self, client, db_session, admin_user):
        resp = client.post(
            "/token",
            data={"username": "admin@test.edu", "password": "admin@123"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "access_token" in data


class TestTokenValidation:
    def test_validate_valid_token(self, client, db_session, admin_user, admin_token):
        resp = client.get(
            "/validate-token",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True

    def test_validate_invalid_token(self, client):
        resp = client.get(
            "/validate-token",
            headers={"Authorization": "Bearer invalidtoken123"},
        )
        assert resp.status_code == 401, resp.text

    def test_validate_no_token(self, client):
        resp = client.get("/validate-token")
        assert resp.status_code == 401, resp.text


class TestRefreshToken:
    def test_refresh_success(self, client, db_session, admin_user):
        login_resp = client.post(
            "/login",
            json={"email": "admin@test.edu", "password": "admin@123"},
        )
        refresh_token = login_resp.json()["refresh_token"]

        resp = client.post(
            "/refresh",
            json={"refresh_token": refresh_token},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "access_token" in data

    def test_refresh_invalid_token(self, client):
        resp = client.post(
            "/refresh",
            json={"refresh_token": "invalid_refresh_token"},
        )
        assert resp.status_code == 401, resp.text


class TestChangePassword:
    def test_change_password_success(self, client, db_session, admin_user):
        login_resp = client.post(
            "/login",
            json={"email": "admin@test.edu", "password": "admin@123"},
        )
        token = login_resp.json()["access_token"]

        resp = client.post(
            "/change-password",
            json={
                "current_password": "admin@123",
                "new_password": "newadmin@123",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200, resp.text

    def test_change_password_wrong_current(self, client, db_session, admin_user):
        login_resp = client.post(
            "/login",
            json={"email": "admin@test.edu", "password": "admin@123"},
        )
        token = login_resp.json()["access_token"]

        resp = client.post(
            "/change-password",
            json={
                "current_password": "wrongpassword",
                "new_password": "newadmin@123",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400, resp.text


class TestLogout:
    def test_logout_success(self, client, db_session, admin_user, admin_token):
        resp = client.post(
            "/logout",
            json={"refresh_token": "", "device_token": None, "all_devices": False},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True
