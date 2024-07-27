import requests
from django.shortcuts import render, get_object_or_404
from .tmdb import search_movies, get_movie_details, get_movie_reviews

GOOGLE_API_KEY = "AIzaSyBIeOjwl6VwoSbUAdTbcS4IXESKUy5lIXM"
SEARCH_ENGINE_ID = "231b66f2d8f54434d"

STREAMING_SERVICES = {
    "netflix.com": {
        "name": "Netflix",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Netflix_logo.svg",
    },
    "hulu.com": {
        "name": "Hulu",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/e/e4/Hulu_Logo.svg",
    },
    "disneyplus.com": {
        "name": "Disney+",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg",
    },
    "amazon.com": {
        "name": "Amazon Prime Video",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png",
    },
    "hbomax.com": {
        "name": "HBO Max",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_Max_Logo.svg",
    },
}


def get_google_search_results(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": SEARCH_ENGINE_ID, "q": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def filter_streaming_results(results):
    filtered_results = []
    for item in results.get("items", []):
        for domain, service in STREAMING_SERVICES.items():
            if domain in item.get("link", ""):
                filtered_results.append(
                    {
                        "name": service["name"],
                        "url": item.get("link"),
                        "logo_url": service["logo_url"],
                        "snippet": item.get("snippet", ""),
                    }
                )
                break
    return filtered_results


def search_view(request):
    query = request.GET.get("q")
    results = []
    message = ""
    if query:
        data = search_movies(query)
        results = data.get("results", [])
        if not results:
            message = f"No movies found for '{query}'"
        else:
            for movie in results:
                # Constructing full poster path URL
                if movie.get("poster_path"):
                    movie["poster_url"] = (
                        f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    )
                else:
                    # If no poster path is available, provide a default image URL or handle it accordingly
                    movie["poster_url"] = (
                        "https://via.placeholder.com/500x750?text=No+Image"
                    )
    return render(request, "search.html", {"results": results, "message": message})


def movie_details_view(request, movie_id):
    movie = get_movie_details(movie_id)
    reviews = get_movie_reviews(movie_id)
    google_results = get_google_search_results(f"{movie['title']} streaming")
    streaming_services = (
        filter_streaming_results(google_results) if google_results else []
    )
    return render(
        request,
        "movie_details.html",
        {"movie": movie, "reviews": reviews, "streaming_services": streaming_services},
    )
