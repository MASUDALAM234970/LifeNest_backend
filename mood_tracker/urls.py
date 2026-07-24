from django.urls import path
from .views import MoodEntryListCreate, MoodEntryDetail, MoodSummaryView

app_name = 'mood_tracker'

urlpatterns = [
    path('entries/', MoodEntryListCreate.as_view(), name='mood-entry-list-create'),
    path('entries/<int:pk>/', MoodEntryDetail.as_view(), name='mood-entry-detail'),
    path('summary/', MoodSummaryView.as_view(), name='mood-summary'),
]