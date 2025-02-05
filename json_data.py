import json
from utils.get_anime import get_anime
from utils.test import load_json_anime
def ciao():
    # File name
    file_name = "data_new.json"

    # Step 1: Read the existing JSON data
    try:
        with open(file_name, "r") as json_file:
            existing_data = json.load(json_file)  # Load existing data
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list or dictionary
        existing_data = []

    new_data = get_anime()
    # Step 2: Modify the data
    # If the existing data is a list, append the new object
    if isinstance(existing_data, list):
        existing_data.append(new_data)
    # If the existing data is a dictionary, merge the new object
    elif isinstance(existing_data, dict):
        existing_data.update(new_data)
    else:
        raise ValueError("Existing JSON data is not a list or dictionary.")

    # Step 3: Write the updated data back to the file
    with open(file_name, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    print(f"New data has been inserted into {file_name}")

def make_anime_response(metadata_anime):
    name = metadata_anime['metadata']['anime']
    anime_json = load_json_anime()
    result = next((item for item in anime_json if item["name"] == name), None)
    caption = f""" Titolo anime : {result['name']}
                \nDescrizione : {result['description']} 
                \nGeneri : {result['genre']} 
                \nDove vederlo : {result['anime_link']}
    """
    return result['image_link'], caption