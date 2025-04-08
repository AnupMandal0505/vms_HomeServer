
from django.urls import path,include

from rest_framework import routers
from .views import LoginAPI,LogoutView,DisplayLoginAPI

router = routers.DefaultRouter()
router.register('login', LoginAPI, basename='login')
router.register('display_login', DisplayLoginAPI, basename='d_login_urls')
router.register('logout', LogoutView, basename='logout')

urlpatterns = router.urls
