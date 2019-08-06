import factory

from ..models import Category, Thing


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category


class ThingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Thing
