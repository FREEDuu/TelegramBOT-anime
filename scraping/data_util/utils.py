import json
import os

def write_json(data, filename):
    """
    Creates a JSON file and writes the provided data to it.

    Args:
        data (dict or list): The data to be written to the JSON file.
        filename (str): The path to the JSON file to be created.
    """
    try:
        # Create the directory if it doesn't exist.
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"JSON data written to '{filename}'.")
    except Exception as e:
        print(f"Error writing JSON to '{filename}': {e}")

def save_image_data_to_json(data, filename):
    """Saves 'parentHref' and 'currentSrc' from image data to a JSON file."""

    extracted_data = []
    for item in data:
        extracted_data.append({
            "tv_url": item.get("parentHref"),  # Use .get() to handle missing keys
            "image": item.get("currentSrc")
        })

    try:
        with open('/home/francesco/Desktop/temp/TelegramBOT-anime/data/films/'+filename, 'w', encoding='utf-8') as outfile:
            json.dump(extracted_data, outfile, indent=4, ensure_ascii=False)
        print(f"Image data saved to '{filename}'.")
    except Exception as e:
        print(f"Error writing to output file: {e}")

def get_parent_hrefs_with_current_src(json_file):
    
    """
    Reads a JSON file, extracts 'parentHref' and 'currentSrc' from each object,
    and returns them in a dictionary where keys are parentHref and values are currentSrc.
    """

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file}'.")
        return None

    result = {}
    for item in data:
        parent_href = item.get("tv_url")
        current_src = item.get("image")

        if parent_href and current_src: 
            result[parent_href] = current_src

    return result