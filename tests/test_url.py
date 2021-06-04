import json
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus


class RestTestCase(TestCase):
    """Test suite for REST endpoints."""

    def setUp(self):
        """Define the test variables."""
        self.client = Client()

    def test_list_all_loggers(self):
        """Test listing all loggers."""
        url = reverse("loggerpanel-list")
        resp = self.client.get(url, HTTP_ACCEPT="application/json")
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertIsInstance(content["log_levels"], dict)
        self.assertIsInstance(content["loggers"], list)

    def test_change_log_level(self):
        """Test change a logger level."""
        previous_level = "WARNING"
        new_level = "DEBUG"
        url = reverse("loggerpanel-detail", kwargs={"logger_name": "root"})

        resp = self.client.get(url, HTTP_ACCEPT="application/json")
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(content["effectiveLevel"]["name"], previous_level)

        resp = self.client.post(
            url, {"logger_level": new_level}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        resp = self.client.get(url, HTTP_ACCEPT="application/json")
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(content["effectiveLevel"]["name"], new_level)
