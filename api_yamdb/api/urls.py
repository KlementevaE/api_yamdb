from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GenreViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet

router_v1 = SimpleRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
