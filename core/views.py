import json
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Game
from core.models.price import Price
from core.serializers.game import GameSerializer
from core.serializers.price import PriceSerializer


class GameAPIView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        try:
            query = Game.objects.get(name=request.data.get('name'))
        except Game.DoesNotExist:
            return Response({'error': 'Not found : {}'.format(request.data.get('name'))},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = GameSerializer(query, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GameAPIPriceView(APIView):
    def put(self, request):
        try:
            query = Game.objects.get(name=request.data.get('name'))
        except Game.DoesNotExist:
            return Response({'error': 'Not found : {}'.format(request.data.get('name'))},
                            status=status.HTTP_400_BAD_REQUEST)
        price = Price.objects.create(**request.data.get('prices'))
        price.save()
        query.prices.add(price)
        query.save()

        return Response(GameSerializer(Game.objects.get(name=request.data.get('name'))).data)
