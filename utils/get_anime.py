import requests

def get_anime():
    anime_request = requests.get('http://127.0.0.1:8000/')
    data = anime_request.json()
    data_load = []
    for anime in data:
        try:
                
            anime['genre'] = ''
            genre_list = requests.get(f'http://127.0.0.1:8000/getGenre/{anime["name"]}').json()
            for genre in genre_list:
                anime['genre'] = anime['genre'] + genre['genre'][0] + ' '
        except:
            pass
        if len(anime['description']) > 30:
            data_load.append(anime)
    return data_load

