# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bands/', views.band_list, name='band_list'),
    path('albums/', views.album_list, name='album_list'),
]
