# search/tmdb.py

import requests

API_KEY = '7eff3eeab9499f45c968ba2c2d437998'  # Replace with your TMDB API key
BASE_URL = 'https://api.themoviedb.org/3'

def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    return response.json()

def get_movie_details(movie_id):
    response = requests.get(f'{BASE_URL}/movie/{movie_id}', params={'api_key': API_KEY})
    movie = response.json()
    if movie.get('poster_path'):
        movie['poster_url'] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
    else:
        movie['poster_url'] = "https://via.placeholder.com/500x750?text=No+Image"
    return movie

def get_movie_reviews(movie_id):
    response = requests.get(f'{BASE_URL}/movie/{movie_id}/reviews', params={'api_key': API_KEY})
    reviews_data = response.json()
    reviews = []
    for review in reviews_data.get('results', []):
        reviews.append({
            'author': review['author'],
            'content': review['content'],
            'url': review['url']
        })
    return reviews