from django.urls import path
from core.views import GameAPIView, GameAPIPriceView

urlpatterns = [
    path('games', GameAPIView.as_view()),
    path('games/addprice', GameAPIPriceView.as_view())
]
