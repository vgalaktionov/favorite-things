from favorite_things.tests.factories import UserFactory
from rest_framework.test import APITestCase

from ..models import Category, Thing
from .factories import CategoryFactory, ThingFactory


class CategoryResourceTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.category = CategoryFactory(user=cls.user, name="cake")
        cls.other_user = UserFactory()
        cls.other_category = CategoryFactory(user=cls.other_user, name="cake")

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_list(self):
        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {"id": 1, "name": "person", "user": None},
                {"id": 2, "name": "place", "user": None},
                {"id": 3, "name": "food", "user": None},
                {"id": self.category.id, "name": "cake", "user": self.user.id},
            ],
        )

    def test_get_single(self):
        response = self.client.get(f"/api/categories/{self.category.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": self.category.id, "name": "cake", "user": self.user.id},
        )

    def test_get_single_other_user_fails(self):
        response = self.client.get(f"/api/categories/{self.other_category.id}/")

        self.assertEqual(response.status_code, 404)

    def test_create(self):
        response = self.client.post("/api/categories/", {"name": "animal"})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Category.objects.filter(name="animal", user=self.user).exists())

    def test_create_invalid_fails(self):
        response = self.client.post("/api/categories/", {})

        self.assertEqual(response.status_code, 400)

    def test_update(self):
        response = self.client.put(
            f"/api/categories/{self.category.id}/", {"name": "candy"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Category.objects.filter(
                id=self.category.id, user=self.user, name="candy"
            ).exists()
        )

    def test_update_other_fails(self):
        response = self.client.put(
            f"/api/categories/{self.other_category.id}/", {"name": "candy"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            Category.objects.filter(
                id=self.other_category.id, user=self.other_user, name="candy"
            ).exists()
        )

    def test_delete(self):
        response = self.client.delete(f"/api/categories/{self.category.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_delete_other_fails(self):
        response = self.client.delete(f"/api/categories/{self.other_category.id}/")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Category.objects.filter(id=self.other_category.id).exists())


class ThingResourceTest(APITestCase):
    DATE_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.other_user = UserFactory()
        cls.thing = ThingFactory(user=cls.user)
        cls.other_thing = ThingFactory(user=cls.other_user)

    def setUp(self):
        self.client.force_login(self.user)

    def assertDictSubset(self, first, second):
        """So we don't need to mock out the audit log."""
        second_sub = {k: v for k, v in second.items() if k in first}
        return self.assertDictEqual(first, second_sub)

    def test_get_list(self):
        new_thing = ThingFactory(user=self.user)
        response = self.client.get("/api/things/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertDictSubset(
            {
                "id": self.thing.id,
                "title": self.thing.title,
                "user": self.user.id,
                "description": self.thing.description,
                "ranking": self.thing.ranking,
                "category": self.thing.category_id,
                "category_string": str(self.thing.category),
                "created_date": self.thing.created_date.strftime(self.DATE_FMT),
                "modified_date": self.thing.modified_date.strftime(self.DATE_FMT),
            },
            response.json()[1],
        )
        self.assertEqual(len(response.json()[1]["audit_log"]), 1)
        self.assertDictSubset(
            {
                "id": new_thing.id,
                "title": new_thing.title,
                "user": self.user.id,
                "description": new_thing.description,
                "ranking": new_thing.ranking,
                "category": new_thing.category_id,
                "category_string": str(new_thing.category),
                "created_date": new_thing.created_date.strftime(self.DATE_FMT),
                "modified_date": new_thing.modified_date.strftime(self.DATE_FMT),
            },
            response.json()[0],
        )
        self.assertEqual(len(response.json()[0]["audit_log"]), 1)

    def test_get_single(self):
        response = self.client.get(f"/api/things/{self.thing.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(
            {
                "id": self.thing.id,
                "title": self.thing.title,
                "user": self.user.id,
                "description": self.thing.description,
                "ranking": self.thing.ranking,
                "category": self.thing.category_id,
                "category_string": str(self.thing.category),
                "created_date": self.thing.created_date.strftime(self.DATE_FMT),
                "modified_date": self.thing.modified_date.strftime(self.DATE_FMT),
            },
            response.json(),
        )
        self.assertEqual(len(response.json()["audit_log"]), 1)

    def test_get_single_other_user_fails(self):
        response = self.client.get(f"/api/things/{self.other_thing.id}/")

        self.assertEqual(response.status_code, 404)

    def test_create(self):
        place = Category.objects.get(name="place")
        response = self.client.post(
            "/api/things/",
            {
                "title": "Foobar",
                "description": "Foo the bar and Baz the qux.",
                "ranking": 2,
                "category": place.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Thing.objects.filter(
                title="Foobar",
                user=self.user,
                description="Foo the bar and Baz the qux.",
                ranking=2,
                category=place,
                metadata={},
            ).exists()
        )

    def test_create_empty_fails(self):
        response = self.client.post("/api/things/", {})

        self.assertEqual(response.status_code, 400)

    def test_create_missing_field_fails(self):
        place = Category.objects.get(name="place")
        response = self.client.post(
            "/api/things/",
            {
                "description": "Foo the bar and Baz the qux.",
                "ranking": 2,
                "category": place.id,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_create_short_description_fails(self):
        place = Category.objects.get(name="place")
        response = self.client.post(
            "/api/things/",
            {"title": "Foobar", "description": "F", "ranking": 2, "category": place.id},
        )

        self.assertEqual(response.status_code, 400)

    def test_update(self):
        response = self.client.put(
            f"/api/things/{self.thing.id}/",
            {
                "title": "banana",
                "ranking": self.thing.ranking,
                "description": self.thing.description,
                "metadata": self.thing.metadata,
                "category": self.thing.category_id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Thing.objects.filter(
                id=self.thing.id, user=self.user, title="banana"
            ).exists()
        )

    def test_update_other_fails(self):
        response = self.client.put(
            f"/api/things/{self.other_thing.id}/", {"title": "banana"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            Thing.objects.filter(
                id=self.other_thing.id, user=self.other_user, title="banana"
            ).exists()
        )

    def test_delete(self):
        response = self.client.delete(f"/api/things/{self.thing.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Thing.objects.filter(id=self.thing.id).exists())

    def test_delete_other_fails(self):
        response = self.client.delete(f"/api/things/{self.other_thing.id}/")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Thing.objects.filter(id=self.other_thing.id).exists())
