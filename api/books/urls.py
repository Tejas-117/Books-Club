from django.urls import path, include
from . import views

app_name = "books"
urlpatterns = [
    # GET all the books & POST a new book
    # Ex: /api/books/
    path("", views.books_controller, name="books_controller"),

    # GET, PUT, DELETE a book
    # Ex: /api/books/1/
    path("<int:book_id>/", views.book_controller, name="book_controller"),
    
    # Add or remove a book from wishlist
    # Ex: /api/books/1/wishlist
    path("<int:book_id>/wishlist/", views.book_wishlist_controller, name="book_wishlist_controller"),
    
    # All Comments endpoint
    # Ex: /api/books/1/comments/
    path("<int:book_id>/comments/", include("comments.urls")),
]
