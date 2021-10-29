from django.db import models


class Specification(models.Model):
    # id = models.AutoField(primary_key=True)
    min = models.TextField()
    max = models.TextField()

    def __str__(self):
        return self.max and self.min
