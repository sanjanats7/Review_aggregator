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
