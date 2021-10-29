from rest_framework import serializers
from core.models.developer import Developer


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'

