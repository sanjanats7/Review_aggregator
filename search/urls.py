# search/urls.py

from django.urls import path
from .views import search_view, movie_details_view

urlpatterns = [
    path('', search_view, name='search'),
    path('movie/<int:movie_id>/', movie_details_view, name='movie_details')
]
