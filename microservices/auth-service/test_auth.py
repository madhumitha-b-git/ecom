import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Mock database at import time
with patch("database.get_db") as mock_get_db:
    from main import app
    client = TestClient(app)


class TestAuthService(unittest.TestCase):
    def test_health(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"service": "auth-service", "status": "ok"})

    @patch("service.get_db")
    def test_register_user_success(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.get_item.return_value = {}  # User does not exist
        mock_get_db.return_value = mock_db

        response = client.post(
            "/v1/auth/register",
            json={
                "name": "Alice",
                "email": "alice@example.com",
                "password": "password123",
                "confirm_password": "password123"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], "alice@example.com")
        self.assertIn("verification_code", response.json())

    @patch("service.get_db")
    def test_get_users_list(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.scan.return_value = {
            "Items": [{"email": "user@example.com", "name": "User", "status": "VERIFIED"}]
        }
        mock_get_db.return_value = mock_db

        token = "dXNlcjEyMzoxNzIwMDAwMDAw"
        response = client.get(
            "/v1/auth/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["email"], "user@example.com")


if __name__ == "__main__":
    unittest.main()
