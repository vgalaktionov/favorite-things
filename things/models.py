import json

from django.contrib.auth import get_user_model

# use the custom jsonfield to avoid conflicts with auditlog
from jsonfield import JSONField
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
    metadata = JSONField(default=dict, encoder_class=DjangoJSONEncoder)
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
        """
        * Add support for datetime in metadata.
        * Automatically re-rank within the same category.
        """

        for key, value in self.metadata.items():
            if isinstance(value, str):
                try:
                    self.metadata[key] = parse(value)
                except ValueError:
                    continue

        exists_with_ranking = Thing.objects.filter(
            ranking=self.ranking, category=self.category
        ).first()
        if exists_with_ranking:
            # recursively re-rank the other things
            exists_with_ranking.ranking += 1
            exists_with_ranking.save()

        return super().save(*args, **kwargs)


auditlog.register(Thing, exclude_fields=["created_date", "modified_date"])
