from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView, TokenObtainPairView

app_name='users'
urlpatterns = [
   # Register the user
   # Ex: /api/users/register/
   path("register/", views.register, name='register'),

   # Get a user with the user_id
   # E: /api/users/1/ <-- 1: user_id
   path("<int:user_id>/", views.user_controller),

   # Endpoints to access auth tokens
   # Ex: /api/users/token/
   path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   
   # Ex: /api/users/token/refresh/
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]