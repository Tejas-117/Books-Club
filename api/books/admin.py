from django.contrib import admin
from books.models import *

admin.site.register(Book)
admin.site.register(Image)
admin.site.register(WishList)