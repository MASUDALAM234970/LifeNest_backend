from rest_framework import serializers


class ChatSerializer(serializers.Serializer):

    message = serializers.CharField()

    language = serializers.ChoiceField(
        choices=[
            "English",
            "Bangla",
            "Hindi",
            "Arabic"
        ]
    )

    history = serializers.ListField(
        required=False,
        default=[]
    )