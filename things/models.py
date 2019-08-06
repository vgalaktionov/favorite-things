from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from dateutil.parser import parse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Thing(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(
        null=True, blank=True, validators=[MinLengthValidator(10)]
    )
    ranking = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    metadata = JSONField(default=dict, encoder=DjangoJSONEncoder)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    audit_log = AuditlogHistoryField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ("category", "ranking", "user"),
            ("category", "title", "user"),
        )

    def __str__(self):
        return f"Thing '{self.title}' for user {self.user}"

    def save(self, *args, **kwargs):
        """Add support for datetime in metadata."""
        for key, value in self.metadata.items():
            if isinstance(value, str):
                try:
                    self.metadata[key] = parse(value)
                except ValueError:
                    continue
        return super().save(*args, **kwargs)


auditlog.register(Thing, exclude_fields=["created_date", "modified_date"])
