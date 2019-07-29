from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from things.models import Category, Thing


class OwnItemsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CategoryViewSet(ModelViewSet):
    def get_queryset(self):
        return Category.objects.filter(user__in=[self.request.user, None])


class ThingViewSet(ModelViewSet):
    def get_queryset(self):
        return Thing.objects.filter(user=self.request.user)
