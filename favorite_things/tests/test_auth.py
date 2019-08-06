from django.test import TestCase, RequestFactory

from ..auth import DummyBackend
from .factories import UserFactory


class AuthTest(TestCase):
    def test_dummy_auth(self):
        user = UserFactory(username="jimbo")
        request = RequestFactory().get("/")

        result = DummyBackend().authenticate(request, username=user.username)

        self.assertEqual(result.id, user.id)
