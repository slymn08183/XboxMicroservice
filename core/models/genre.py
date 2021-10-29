from django.db import models


class Genre(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.TextField()

    def __str__(self):
        return self.title

