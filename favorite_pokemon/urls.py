from django.urls import path
from . import views

app_name = 'favorite_pokemon'

urlpatterns = [
   path('', views.index_view, name="favorite.index"),
]
