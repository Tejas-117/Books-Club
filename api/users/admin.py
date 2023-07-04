from django.contrib import admin

from users.models import User, Tag, UserImage

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(UserImage)