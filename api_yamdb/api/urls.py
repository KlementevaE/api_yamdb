from django.urls import include, path
from rest_framework import routers

import api.views as views

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', views.UserViewSet, basename="users")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.AuthSignupView.as_view()),
    path('v1/auth/token/',
         views.AuthTokenView.as_view(), name='token_obtain_pair'
         ),
]
