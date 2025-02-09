import json

def save_urls_to_json(url_list, filename="tv_series_urls_data.json", series_name="TV Series"):
    """Saves a list of URLs to a JSON file, grouping them under a series name.

    Args:
        url_list: A list of URLs.
        filename: The name of the JSON file to save to (default: "tv_series_urls.json").
        series_name: The name to use for the TV series in the JSON (default: "TV Series").
    """

    tv_series_data = {series_name: url_list}  # Create the dictionary

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tv_series_data, f, indent=4, ensure_ascii=False)

        print(f"URLs saved to {filename}")

    except Exception as e:
        print(f"Error saving URLs to JSON: {e}")