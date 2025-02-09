import json
import re

def merge_json_files(file1, file2, file3):
    """
    Merges two JSON files, adds 'currentSrc' if match found, and fills/cleans titles.
    """

    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
    except FileNotFoundError:
        print(f"Error: File '{file1}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file1}'.")
        return

    try:
        with open(file2, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
    except FileNotFoundError:
        print(f"Error: File '{file2}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file2}'.")
        return

    merged_data = []

    for item1 in data1:
        new_item = item1.copy()

        # Clean title (remove number prefix if present)
        current_title = new_item.get("title")
        if current_title:
            new_item["title"] = re.sub(r"^\d+-", "", current_title).strip() # added .strip()

        # Fill empty titles from URL
        if not new_item.get("title"):
            url_part = new_item.get("url").split('/')[-1]
            new_item["title"] = re.sub(r"^\d+-", "", url_part).strip() # added .strip()


        for item2 in data2:
            if item1.get("url") == item2.get("parentHref"):
                new_item["currentSrc"] = item2.get("currentSrc")
                break

        merged_data.append(new_item)

    try:
        with open(file3, 'w', encoding='utf-8') as f3:
            json.dump(merged_data, f3, indent=4, ensure_ascii=False)
        print(f"Merged data saved to '{file3}'.")
    except Exception as e:
        print(f"Error writing to file: {e}")


# Example usage:
file1_name = "1film.json"
file2_name = "2film.json"
file3_name = "3film.json"

merge_json_files(file1_name, file2_name, file3_name)