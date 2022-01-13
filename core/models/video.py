from django.db import models


class Video(models.Model):
    # id = models.AutoField(primary_key=True)
    url = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.url
