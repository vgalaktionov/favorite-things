from django.db.models import Q

from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from things.models import Category, Thing
from things.serializers import CategorySerializer, ThingSerializer


class OwnItemsPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if obj.user is None:
            return request.method not in ('PUT', 'POST', 'PATCH', 'DELETE')
        return obj.user == request.user


class ForUserMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(ModelViewSet, ForUserMixin):
    serializer_class = CategorySerializer
    permission_classes = [OwnItemsPermission]

    def get_queryset(self):
        return Category.objects.filter(Q(user=self.request.user) | Q(user__isnull=True))


class ThingViewSet(ModelViewSet, ForUserMixin):
    serializer_class = ThingSerializer
    permission_classes = [OwnItemsPermission]

    def get_queryset(self):
        return Thing.objects.filter(user=self.request.user)
