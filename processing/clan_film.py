import json
import re

def process_json(input_file, output_file):
    """
    Processes a JSON input file, adding the URL (without number prefix) as the title
    if the title is empty, and writes the result to a new JSON output file.
    """

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{input_file}'.")
        return

    processed_data = []
    for item in data:
        new_item = item.copy()  # Create a copy to avoid modifying the original data
        if not new_item['title']:
          url_part = new_item['url'].split('/')[-1]
          # Remove the number prefix (e.g., "9898-something" becomes "something")
          url_part = re.sub(r'^\d+-', '', url_part)
          new_item['title'] = url_part
        processed_data.append(new_item)

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(processed_data, outfile, indent=4, ensure_ascii=False)
        print(f"Processed data written to '{output_file}'.")
    except Exception as e:
        print(f"Error writing to output file: {e}")


# Example usage:
input_filename = 'scraped_data.json'  # Replace with your input file name
output_filename = 'output.json'  # Replace with your desired output file name

process_json(input_filename, output_filename)
