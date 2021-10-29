import datetime
from django.db import models


class Price(models.Model):
    # id = models.AutoField(primary_key=True)
    discount = models.CharField(max_length=10, null=False)
    original = models.CharField(max_length=10, null=False)
    discount_fmt = models.CharField(max_length=15, null=False)
    original_fmt = models.CharField(max_length=15, null=False)
    createdAt = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.discount, self.original, self.discount_fmt, self.original_fmt, self.createdAt
