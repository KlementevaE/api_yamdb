from django.shortcuts import get_object_or_404
from rest_framework import (response, status,
                            viewsets,
                            permissions,
                            filters)
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (UserSerializer, UserMeSerializer,
                          AuthSignupSerializer, AuthTokenSerializer)
from .permissions import AdminPermission  # , SelfPermission
from .pagination import UserPagination
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Viewset для эндпоинтов users и users/me."""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = (AdminPermission,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('username',)

    @action(methods=['get', 'patch'], detail=False,
            url_path='me', permission_classes=[permissions.IsAuthenticated, ],
            )
    def me(self, request):
        user = User.objects.get(username=self.request.user)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        message = {
            "Message": "Ошибочно заданы параметры",
        }
        return response.Response(
            data=message,
            status=status.HTTP_400_BAD_REQUEST
        )


class AuthSignupView(CreateAPIView):
    """Generic для самостоятельной регистрации.
    И получения кода подтверждения"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class AuthTokenView(CreateAPIView):
    """Generic для получения access-токена."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        code = serializer.validated_data["confirmation_code"]
        user = get_object_or_404(User.objects.all(), username=username)
        if user.confirmation_code == code:
            token = AccessToken.for_user(user)
            res = {
                "token": str(token),
            }
            return response.Response(res, status.HTTP_201_CREATED)
        message = {
            "Message": "Ошибочный confirmation_code",
        }
        return response.Response(
            data=message,
            status=status.HTTP_400_BAD_REQUEST
        )
