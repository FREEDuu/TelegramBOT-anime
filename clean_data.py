import json

# Define the names of your input and output files
input_files = ['3film.json', '3.json']

for filename in input_files:

    # Step 1: Read the JSON data from the input file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Step 2: Modify the data
    for item in data:
        if 'url' in item:
            item['url'] = item['url'].replace('streamingcommunity.paris', 'streamingcommunityz.bid/en')
        if 'currentSrc' in item:
            item['currentSrc'] = item['currentSrc'].replace('streamingcommunity.paris', 'streamingcommunityz.bid')

    # Step 3: Write the modified data to a new JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data from '{file}' has been modified")