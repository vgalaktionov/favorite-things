from django.conf import settings
from django.test import TestCase

from .factories import UserFactory


class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_unauthenticated_index_redirects_to_login(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login")

    def test_authenticated_index_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_login_authenticates(self):
        response = self.client.get("/auth/login")

        self.assertEqual(response.status_code, 200)

        response = self.client.post("/auth/login", {"username": self.user.username})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_logout_redirects(self):
        self.client.force_login(self.user)
        response = self.client.get("/auth/logout")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGOUT_REDIRECT_URL)
