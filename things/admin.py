from django.contrib import admin

from things.models import Category, Thing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]

    def has_change_permission(self, request, obj=None):
        if obj and obj.name in ("person", "place", "food"):
            return False
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.name in ("person", "place", "food"):
            return False
        return super().has_delete_permission(request, obj=obj)


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ["title", "ranking", "category", "created_date", "modified_date"]
