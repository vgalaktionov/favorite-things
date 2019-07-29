from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator, MinValueValidator

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog


class Category(models.Model):
    name = models.CharField(max_length=100)


class Thing(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True, validators=[MinLengthValidator(10)])
    ranking = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    metadata = JSONField(default=dict)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    audit_log = AuditlogHistoryField()

    class Meta:
        unique_together = ('category', 'ranking')


auditlog.register(Thing, exclude_fields=['created_date', 'modified_date'])
