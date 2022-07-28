from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryList, CategoryDetail, GenreList, GenreDetail, TitleViewSet

router_v1 = SimpleRouter()
router_v1.register(r'titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/categories/', CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', CategoryDetail.as_view()),
    path('v1/genres/', GenreList.as_view()),
    path('v1/genres/<slug:slug>/', GenreDetail.as_view()),
]
