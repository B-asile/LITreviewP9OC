from django.urls import path
from .views import home, create_ticket, create_review, follow_users, edit_ticket, reply_to_ticket, delete_followed, \
    delete_ticket, posts, edit_review, delete_review

urlpatterns = [
    path("home", home, name="home"),
    path("posts", posts, name="posts"),
    path("ticket", create_ticket, name="reviews-create_ticket"),
    path("review", create_review, name="reviews-create_review"),

    path("followUser", follow_users, name="reviews-follow_user"),
    path("follower/<int:followed_user_id>/delete", delete_followed, name="delete_followed"),

    path("ticket/<int:ticket_id>/edit", edit_ticket, name="reviews_edit"),
    path("ticket/<int:ticket_id>/delete", delete_ticket, name="delete_ticket"),
    path("ticket/<int:ticket_id>/replyToTicket", reply_to_ticket, name="reviews_reply_to_ticket"),

    path("review/<int:review_id>/edit", edit_review, name="edit_review"),
    path("review/<int:review_id>/delete", delete_review, name="delete_review"),
]