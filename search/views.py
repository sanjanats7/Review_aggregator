from django.shortcuts import render
from .tmdb import search_movies

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        data = search_movies(query)
        results = data.get('results', [])
        for movie in results:
            # Constructing full poster path URL
            if movie.get('poster_path'):
                movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            else:
                # If no poster path is available, you can provide a default image URL or handle it accordingly
                movie['poster_url'] = "https://via.placeholder.com/500x750?text=No+Image"
    return render(request, 'search.html', {'results': results})
