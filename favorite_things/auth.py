import os

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class DummyBackend:
    def authenticate(self, request, username=None, password=None):
        if username:
            user, _ = User.objects.get_or_create(
                username=username,
                is_staff=False,
                is_superuser=False
            )
            return user
        return None

    def get_user(self, id):
        return User.objects.get(id=id)
