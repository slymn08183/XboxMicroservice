from django.urls import path
from core.views import GameAPIView

urlpatterns = [
    path('games', GameAPIView.as_view())
]
