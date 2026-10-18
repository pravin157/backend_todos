"""
API views for user authentication and task management.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    TodoSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    """Handles new user registration and token generation."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user': UserSerializer(user).data,
                    'message': 'Registration successful',
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handles user login via username or email."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            # Support logging in with email address as well
            try:
                user_obj = User.objects.get(email__iexact=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user': UserSerializer(user).data,
                    'message': 'Login successful',
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {'detail': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    """Handles user logout by deleting the auth token."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response(
            {'message': 'Logged out successfully.'},
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    """Returns the authenticated user's profile."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class TodoViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for user-scoped Todo tasks.
    Guarantees private data isolation per authenticated user.
    """

    serializer_class = TodoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            # Strictly return ONLY tasks owned by the authenticated user
            return Todo.objects.filter(user=user)
        # Unauthenticated requests see an empty list (no data leak)
        return Todo.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
