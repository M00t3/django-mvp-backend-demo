from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, LoginSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@extend_schema(
    tags=['Auth'],
    request=RegisterSerializer,
    responses={201: dict},
    summary="Register a new user",
    description="Register a new user and return JWT access and refresh tokens"
)
class RegisterAPIView(APIView):
    """
    API endpoint to register a new user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Create a new user with username, email, and password.
        Returns access and refresh tokens.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Auth'],
    request=LoginSerializer,
    responses={200: dict},
    summary="Login user",
    description="Login with username and password to get JWT access and refresh tokens"
)
class LoginAPIView(APIView):
    """
    API endpoint to authenticate a user.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Authenticate with username and password to obtain JWT access and refresh tokens.
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
