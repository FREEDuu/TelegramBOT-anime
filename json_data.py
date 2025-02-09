import json

def load_json(filename):
    # Step 1: Open the JSON file
    with open(filename, 'r') as file:
        # Step 2: Load the JSON data
        data = json.load(file)

    # Now `data` is a Python dictionary (or list, depending on the JSON structure)
    return (data)

def load_json_anime():
    # Step 1: Open the JSON file
    with open('anime.json', 'r') as file:
        # Step 2: Load the JSON data
        data = json.load(file)
    return data[0]

def make_anime_response(metadata_anime):
    name = metadata_anime['metadata']['anime']
    anime_json = load_json_anime()
    result = next((item for item in anime_json if item["name"] == name), None)
    caption = f"""✨ Titolo Anime: {result['name']}  
    📝 Descrizione: {result['description']}  
    🎭 Generi: {result['genre']}  
    📺 Dove vederlo: {result['anime_link']}  
    """

    return result['image_link'], caption

def make_tvfilm_response(metadata_film, filename):
    title = metadata_film['metadata']['title']
    anime_json = load_json(filename)
    result = next((item for item in anime_json if item["title"] == title), None)
    specs = result['specs'].split('-')[:2]
    caption = f"""🎬 Titolo: {result['title']}  
    📅 Anno: {specs[0]} | ⏳ Durata: {specs[1]}  
    📝 Descrizione: {result['description']}  
    🎭 Generi: {result['genre']}  
    📺 Dove vederlo: {result['url']}  
    """

    return result['currentSrc'], caption

def make_film_response(metadata_film, filename):
    return make_tvfilm_response(metadata_film, filename)
def make_tv_response(metadata_film, filename):
    return make_tvfilm_response(metadata_film, filename)