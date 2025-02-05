import json

def ciao(data):
    # File name
    file_name = "data/data_new2.json"

    # Step 1: Read the existing JSON data
    try:
        with open(file_name, "r") as json_file:
            existing_data = json.load(json_file)  # Load existing data
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list or dictionary
        existing_data = []

    new_data = data
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


def load_json_anime():
    # Step 1: Open the JSON file
    with open('data/data_new2.json', 'r') as file:
        # Step 2: Load the JSON data
        data = json.load(file)

    # Now `data` is a Python dictionary (or list, depending on the JSON structure)
    return (data[0])

def clean_json():
    anime_json = load_json_anime()
    cleaned = clean_anime_list(anime_json)
    cleaned = [anime for anime in cleaned if len(anime['description']) > 200]


def get_main_title(name):
    """Extract the main title before any colon or special characters"""
    return name.split(':')[0].strip()

def has_common_words(name1, name2, min_words=2):
    """Check if two names share enough common words"""
    # Convert to lowercase and split into words
    words1 = set(name1.lower().split())
    words2 = set(name2.lower().split())
    
    # Find common words
    common = words1.intersection(words2)
    
    # Return True if we have at least min_words in common
    return len(common) >= min_words

def clean_anime_list(anime_list):
    """
    Quickly clean and group similar anime entries.
    Returns list of unique anime with shortest/base names.
    """
    # Group by main title
    groups = {}
    
    for anime in anime_list:
        name = anime['name']
        main_title = get_main_title(name)
        
        # If we already have this main title, check if current name is shorter
        if main_title in groups:
            if len(name) < len(groups[main_title]['name']):
                groups[main_title] = anime
        else:
            # Check if we have similar entries based on common words
            similar_found = False
            for existing_title in list(groups.keys()):  # Create list to avoid runtime modification issues
                if has_common_words(main_title, existing_title):
                    # If found similar, keep the shorter name
                    if len(name) < len(groups[existing_title]['name']):
                        groups[existing_title] = anime
                    similar_found = True
                    break
            
            # If no similar entries found, add as new group
            if not similar_found:
                groups[main_title] = anime
    
    return list(groups.values())

clean_json()