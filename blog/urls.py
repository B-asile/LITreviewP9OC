from django.urls import path
from .views import home, create_ticket, create_review, follow_users, edit_ticket, reply_to_ticket, delete_followed

urlpatterns = [
    path("home", home, name="home"),
    path("ticket", create_ticket, name="reviews-create_ticket"),
    path("review", create_review, name="reviews-create_review"),

    path("followUser", follow_users, name="reviews-follow_user"),
    #path("followUser/<int:followed_user_id>", delete_followed, name="delete_followed"),

    path("<int:ticket_id>/edit", edit_ticket, name="reviews_edit"),
    path("<int:ticket_id>/replyToTicket", reply_to_ticket, name="reviews_reply_to_ticket"),
]