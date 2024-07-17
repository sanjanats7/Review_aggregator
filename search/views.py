# search/views.py

from django.shortcuts import render
from .tmdb import search_movies

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        data = search_movies(query)
        results = data.get('results', [])
    return render(request, 'search.html', {'results': results})
