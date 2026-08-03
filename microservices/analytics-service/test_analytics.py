import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from main import app
client = TestClient(app)


class TestAnalyticsService(unittest.TestCase):
    def test_health(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"service": "analytics-service", "status": "ok"})

    @patch("database.get_stage_data")
    def test_get_revenue(self, mock_get_stage_data):
        mock_get_stage_data.return_value = {"total_revenue": 500.0, "total_orders": 5}
        response = client.get("/v1/analytics/company/revenue")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_revenue"], 500.0)

    @patch("database.get_stage_data")
    def test_get_abandoned_carts(self, mock_get_stage_data):
        mock_get_stage_data.return_value = {"abandoned_count": 2, "abandoned_carts": []}
        response = client.get("/v1/analytics/customer/abandoned-carts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["abandoned_count"], 2)

    @patch("database.get_stage_data")
    def test_get_reliability_metrics(self, mock_get_stage_data):
        mock_get_stage_data.return_value = {"success_rate_percent": 98.5, "average_tat_seconds": 12.0}
        response = client.get("/v1/analytics/engineer/reliability")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success_rate_percent"], 98.5)


if __name__ == "__main__":
    unittest.main()
