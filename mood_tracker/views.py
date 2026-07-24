from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MoodEntry
from .serializers import MoodEntrySerializer, MoodSummarySerializer


class MoodEntryListCreate(generics.ListCreateAPIView):
    serializer_class = MoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        today = timezone.localdate()

        # Only one mood entry per day
        if MoodEntry.objects.filter(
            user=self.request.user,
            date=today,
        ).exists():
            raise serializers.ValidationError({
                "message": "You already added today's mood."
            })

        serializer.save(
            user=self.request.user,
            date=today,
        )


class MoodEntryDetail(generics.RetrieveAPIView):
    serializer_class = MoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)


class MoodSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            days = int(request.query_params.get("days", 7))
        except ValueError:
            return Response(
                {"message": "Days must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=days - 1)

        moods = MoodEntry.objects.filter(
            user=request.user,
            date__range=[start_date, end_date],
        )

        if not moods.exists():
            return Response(
                {
                    "average_mood": None,
                    "most_frequent_emotion": None,
                    "mood_counts": {},
                },
                status=status.HTTP_200_OK,
            )

        mood_counts = (
            moods.values("mood")
            .annotate(count=Count("mood"))
            .order_by("-count")
        )

        most_frequent = mood_counts.first()["mood"]

        mood_mapping = {
            "sad": 1,
            "anxious": 2,
            "angry": 2,
            "neutral": 3,
            "happy": 4,
        }

        total = sum(
            mood_mapping.get(entry.mood, 0)
            for entry in moods
        )

        average_score = total / moods.count()

        if average_score >= 3.5:
            average = "Happy"
        elif average_score >= 2.5:
            average = "Neutral"
        else:
            average = "Sad"

        data = {
            "average_mood": average,
            "most_frequent_emotion": most_frequent,
            "mood_counts": {
                item["mood"]: item["count"]
                for item in mood_counts
            },
        }

        serializer = MoodSummarySerializer(data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )