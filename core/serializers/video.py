from rest_framework import serializers
from core.models.video import Video
from core.serializers import GameSerializer


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

