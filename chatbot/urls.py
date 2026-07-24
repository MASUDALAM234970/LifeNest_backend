from django.urls import path
from .views import MentalHealthChatAPIView

urlpatterns = [
    path(
        "chat/",
        MentalHealthChatAPIView.as_view(),
        name="mental-health-chat",
    ),
]