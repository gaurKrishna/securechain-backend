from django.urls import path
from .views import SignUpAPI, LoginAPI, LogoutApi

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
    path("signup/", SignUpAPI.as_view(), name="signup")
]