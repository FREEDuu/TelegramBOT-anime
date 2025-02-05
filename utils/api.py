import requests
import random
import os

URL = os.getenv('url')

def get_casual_anime():
    resp = requests.get(URL)
    anime = resp.json()[random.randint(0, len(resp.json()))]
    genre_caption = ', '.join([genre[0] for genre in get_anime_genre(anime['name'])])
    caption =  f"""
    Anime : {anime['name']}\n\nGeneri : {genre_caption}\n\nDescrizione : {anime['description']}\n\nPer guardarlo vai al : {anime['anime_link']}\n"""
    return anime['image_link'], caption

def get_anime_genre(anime_name):
    resp = requests.get(f'{URL}getGenre/{anime_name}')
    genre = [ gen['genre'] for gen in resp.json()]
    return genre