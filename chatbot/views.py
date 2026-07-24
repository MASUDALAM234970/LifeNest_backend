from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChatSerializer
from .services import generate_reply


class MentalHealthChatAPIView(APIView):

    def post(self, request):

        serializer = ChatSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        language = serializer.validated_data["language"]
        history = serializer.validated_data.get("history", [])

        reply = generate_reply(
            message=message,
            history=history,
            language=language
        )

        return Response(
            {
                "success": True,
                "reply": reply
            },
            status=status.HTTP_200_OK
        )