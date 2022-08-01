from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, permissions, response, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .pagination import UserPagination
from .permissions import (AdminPermission, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnlyPermission)
from .serializers import (AuthSignupSerializer, AuthTokenSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateUpdateSerializer, TitleReadSerializer,
                          UserMeSerializer, UserSerializer)


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


class AuthSignupView(generics.CreateAPIView):
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


class AuthTokenView(generics.CreateAPIView):
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


class CategoryList(generics.ListCreateAPIView):
    """Generic для эндпоинта categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDetail(generics.DestroyAPIView):
    """Generic для эндпоинта categories/<slug:slug>."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    lookup_field = 'slug'


class GenreList(generics.ListCreateAPIView):
    """Generic для эндпоинта genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDetail(generics.DestroyAPIView):
    """Generic для эндпоинта genres/<slug:slug>."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для эндпоинта titles."""

    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return TitleReadSerializer
        return TitleCreateUpdateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для эндпоинта reviews."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для эндпоинта comments."""

    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
