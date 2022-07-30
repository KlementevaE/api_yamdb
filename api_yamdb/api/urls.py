from django.urls import include, path
from rest_framework import routers

import api.views as views

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', views.UserViewSet, basename="users")
router_v1.register(r'titles', views.TitleViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   views.ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.AuthSignupView.as_view()),
    path('v1/auth/token/',
         views.AuthTokenView.as_view(), name='token_obtain_pair'
         ),
    path('v1/categories/', views.CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', views.CategoryDetail.as_view()),
    path('v1/genres/', views.GenreList.as_view()),
    path('v1/genres/<slug:slug>/', views.GenreDetail.as_view()),
]
