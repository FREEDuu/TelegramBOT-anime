import json

def count_missing_images(json_file):
    """Counts the number of objects in a JSON file that are missing the 'img' attribute."""

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return None  # Or raise an exception if you prefer
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file}'.")
        return None

    count = 0
    for item in data:
        if "img" not in item or not item["img"]:  # Check if 'img' is missing or empty
            count += 1

    return count

# Example usage:
filename = 'TV_images.json'  # Replace with the actual file name
missing_count = count_missing_images(filename)

if missing_count is not None:
    print(f"Number of objects with missing or empty 'img' attribute: {missing_count}")