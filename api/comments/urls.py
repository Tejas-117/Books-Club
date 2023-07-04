from django.urls import path
from . import views

app_name = "comments"
urlpatterns = [
    # POST comment
    # Ex: /api/books/1/comments/
    path("", views.comment_post_controller, name="comment_controller"),
    
    # PUT and DELETE a comment
    # Ex: /api/books/1/comments/1/
    path(
        "<int:comment_id>/",
        views.comment_update_controller,
        name="comment_update_controller",
    ),
]
