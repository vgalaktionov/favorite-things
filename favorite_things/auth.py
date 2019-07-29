import os

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminBackend:
    def authenticate(self, request, username=None, password=None):
        """Hardcoded admin user."""
        if username == settings.ADMIN_USERNAME and password == os.environ.get('ADMIN_PASSWORD'):
            return self.get_user()
        return None

    def get_user(self, _id=None):
        """Id is unused and just there to conform to the interface."""
        user, _ = User.objects.get_or_create(
            username=settings.ADMIN_USERNAME,
            is_staff=True,
            is_superuser=True
        )
        return user


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
