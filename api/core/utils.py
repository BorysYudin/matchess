from .serializers import UserSerializer


def signup_response_handler(token, user=None, request=None):
    return {
        'token': token,
        **UserSerializer(user, context={'request': request}).data
    }
