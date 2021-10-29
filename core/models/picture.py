from django.db import models


class Picture(models.Model):
    # id = models.AutoField(primary_key=True)
    url = models.TextField()

    def __str__(self):
        return self.url
