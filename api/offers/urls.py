from django.urls import path

from . import views

app_name="offers"
urlpatterns = [
   # GET and POST offers
   # Ex: /api/offers/
   path("", views.offers_controller),

   # EDIT and DELETE offer
   path("<int:offer_id>/", views.offer_controller)
]