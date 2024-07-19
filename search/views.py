from django.shortcuts import render, get_object_or_404
from .tmdb import search_movies, get_movie_details, get_movie_reviews

def search_view(request):
    query = request.GET.get('q')
    results = []
    message = ''
    if query:
        data = search_movies(query)
        results = data.get('results', [])
        if not results:
            message = f"No movies found for '{query}'"
        else:
            for movie in results:
                # Constructing full poster path URL
                if movie.get('poster_path'):
                    movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                else:
                    # If no poster path is available, provide a default image URL or handle it accordingly
                    movie['poster_url'] = "https://via.placeholder.com/500x750?text=No+Image"
    return render(request, 'search.html', {'results': results, 'message': message})

def movie_details_view(request, movie_id):
    movie = get_movie_details(movie_id)
    reviews = get_movie_reviews(movie_id)
    return render(request, 'movie_details.html', {'movie': movie, 'reviews': reviews})