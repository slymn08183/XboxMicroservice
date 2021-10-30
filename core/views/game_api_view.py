from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Game
from core.serializers.game import GameSerializer


class GameAPIView(APIView):
    @staticmethod
    def get(request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = GameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def put(request):
        try:
            query = Game.objects.get(name=request.data.get('name'))
        except Game.DoesNotExist:
            return Response({'error': 'Not found : {}'.format(request.data.get('name'))},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = GameSerializer(query, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

