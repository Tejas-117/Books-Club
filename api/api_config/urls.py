from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Default admin functionalities
    path("admin/", admin.site.urls),

    path("api/", include([
        # Authentication API
        path("users/", include("users.urls")),
        
        # Books API and comments API nested
        path("books/", include("books.urls")),

        # Offers API
        path("offers/", include("offers.urls"))
    ]))
]