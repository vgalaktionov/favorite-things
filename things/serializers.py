from rest_framework import serializers
from things.models import Category, Thing


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ThingSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    metadata = serializers.JSONField()

    class Meta:
        model = Thing
        read_only_fields = [
            'created_date',
            'modified_date',
        ]
        fields = [
            'title',
            'description',
            'ranking',
            'metadata',
            'category',
            'user'
        ] + read_only_fields
