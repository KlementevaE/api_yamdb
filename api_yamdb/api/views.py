from random import choice
from django.core.mail import send_mail
from rest_framework import response, status
from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    AuthSignupSerializer,
    AuthTokenSerializer
)
from .permissions import AdminPermission, SelfPermission
from reviews.models import User


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class AuthSignupView(CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSignupSerializer

    def generate_confirmation_code(self):
        pool = "1234567890"
        random_str = []
        for _ in range(4):
            random_str.append(choice(pool))
        return "".join(random_str)

    def perform_create(self, serializer):
        to_email = []
        to_email.append(serializer.validated_data["email"])
        code = self.generate_confirmation_code()
        send_mail(
            subject='YaMDB confirmation code ',
            message=f' Your confirmation code is: {code}.',
            from_email='yamdb@yamdb.fake',
            recipient_list=to_email,
            fail_silently=False
        )
        serializer.save(confirmation_code=code)


class AuthTokenView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def perform_create(self, serializer):
        user = serializer.instance.username
        refresh = RefreshToken.for_user(user)
        res = {
            'token': str(refresh.access_token),
        }
        return response.Response(res, status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (OwnerOrReadOnly,)
    permission_classes = (AdminPermission,)

    @action(methods=['get', 'patch'], detail=False,
            url_path='me', permission_classes=[SelfPermission, ]
            )
    def me(self, request):
        print(self.request.user)
        user = User.objects.get(self.request.user)
        # user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
