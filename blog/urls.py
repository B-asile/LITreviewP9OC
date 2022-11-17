from django.urls import path
from .views import home, create_ticket, create_review, follow_users

urlpatterns = [
    path("home", home, name="home"),
    path("ticket", create_ticket, name="reviews-create_ticket"),
    path("review", create_review, name="reviews-create_review"),
    path("followUser", follow_users, name="reviews-follow_user"),
]