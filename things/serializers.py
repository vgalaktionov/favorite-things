from rest_framework import serializers

from things.models import Category, Thing


class CreateWithUserMixin:
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(**validated_data)


class CategorySerializer(serializers.ModelSerializer, CreateWithUserMixin):
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Category
        read_only_fields = ["user"]
        fields = "__all__"


class ThingSerializer(serializers.ModelSerializer, CreateWithUserMixin):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_string = serializers.StringRelatedField(
        required=False, read_only=True, source="category"
    )
    metadata = serializers.JSONField()
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Thing
        read_only_fields = ["created_date", "modified_date", "user", "category_string"]
        fields = [
            "title",
            "description",
            "ranking",
            "metadata",
            "category",
        ] + read_only_fields
