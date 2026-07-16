from rest_framework.authentication import BaseAuthentication


class FirebaseAuthentication(BaseAuthentication):
    """
    Placeholder authentication class.

    Firebase authentication will be implemented later.
    """

    def authenticate(self, request):
        # Returning None means this authentication backend
        # does not authenticate the request.
        return None