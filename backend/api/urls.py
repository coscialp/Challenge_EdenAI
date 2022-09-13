from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
#
from .views import RegisterView, UserViewSet, FileViewSet

router = routers.SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('files', FileViewSet, basename='files')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('', include(router.urls), name='users_list'),
]