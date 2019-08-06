import factory

from ..models import Category, Thing


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category


class ThingFactory(factory.DjangoModelFactory):
    title = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    ranking = 1
    metadata = factory.Faker("pydict")
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Thing
