from django.urls import path
from .views import login_page, signup, logout_user

urlpatterns = [
    path("", login_page, name="authentication_login_page"),
    path("signup", signup, name="signup"),
    path("logout_user", logout_user, name="logout_user"),
]