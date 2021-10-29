from rest_framework import serializers
from core.models.publisher import Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

