from core.models.price import Price
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Game
from core.serializers.game import GameSerializer


class GameAPIPriceView(APIView):
    @staticmethod
    def put(request):
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
