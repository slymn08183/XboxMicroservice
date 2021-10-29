import datetime
from django.db import models

from core.models.description import Description
from core.models.developer import Developer
from core.models.feature import Feature
from core.models.genre import Genre
from core.models.picture import Picture
from core.models.price import Price
from core.models.publisher import Publisher
from core.models.specification import Specification
from core.models.video import Video


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True, blank=False, null=False)
    thumbnail = models.CharField(max_length=2000, blank=False, null=False)
    releaseDate = models.DateTimeField(null=False)
    createdAt = models.DateTimeField(default=datetime.datetime.now)
    isDeleted = models.BooleanField(default=0)

    description = models.ForeignKey(
        Description, on_delete=models.CASCADE, null=True
    )

    specification = models.ForeignKey(
        Specification, on_delete=models.CASCADE, null=True
    )

    videos = models.ManyToManyField(
        Video
    )

    pictures = models.ManyToManyField(
        Picture
    )

    developers = models.ManyToManyField(
        Developer
    )

    features = models.ManyToManyField(
        Feature
    )

    genres = models.ManyToManyField(
        Genre
    )

    prices = models.ManyToManyField(
        Price
    )

    publishers = models.ManyToManyField(
        Publisher
    )

    def __str__(self):
        return self.name




