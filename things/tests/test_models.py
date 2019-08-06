from datetime import datetime

from django.test import TestCase

from favorite_things.tests.factories import UserFactory

from ..models import Category, Thing
from .factories import CategoryFactory


class CategoryModelTest(TestCase):
    def test_create_valid_category(self):
        # should not raise
        Category.objects.create(name="vegetables")
        user = UserFactory()
        Category.objects.create(name="fruits", user=user)


class ThingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.category = CategoryFactory(name="pets")

    def test_create_valid_thing(self):
        # should not raise
        Thing.objects.create(
            title="A thing",
            description="A long description",
            ranking=1,
            metadata={"a": "b", "c": 1},
            category=self.category,
            user=self.user,
        )
        Thing.objects.create(
            title="No description no meta",
            ranking=2,
            category=self.category,
            user=self.user,
        )

    def test_datetime_parsing(self):
        thing = Thing.objects.create(
            title="A thing",
            description="A long description",
            ranking=1,
            metadata={"d": "21 June 2019"},
            category=self.category,
            user=self.user,
        )

        self.assertEqual(thing.metadata["d"], datetime(2019, 6, 21))

    def test_automatic_reordering_within_same_category(self):
        thing1 = Thing.objects.create(
            title="Foo", ranking=1, category=self.category, user=self.user
        )
        thing2 = Thing.objects.create(
            title="Bar", ranking=1, category=self.category, user=self.user
        )
        Thing.objects.create(
            title="Baz", ranking=1, category=self.category, user=self.user
        )

        thing1.refresh_from_db()
        self.assertEqual(thing1.ranking, 3)

        thing2.refresh_from_db()
        self.assertEqual(thing2.ranking, 2)
