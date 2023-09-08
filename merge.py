import json

# Load the items data from the JSON file
with open('items.json', 'r') as items_file:
    items_data = json.load(items_file)

# Load the descriptions data from the JSON file
with open('descriptions.json', 'r') as descriptions_file:
    descriptions_data = json.load(descriptions_file)

# Function to replace DescriptionID with the corresponding description
def replace_description(location):
    description_id = item.get("DescriptionID")
    if description_id:
        description = descriptions_data.get("Descriptions", {}).get(description_id)
        if description:
            item["Description"] = description

# Iterate through each item and replace the DescriptionID with the description
for item in items_data.get("Items", []):
    replace_description(item)

# Write the updated locations data to a new file called "desc.json"
with open('desc.json', 'w') as desc_file:
    json.dump(items_data, desc_file, indent=2)

print("Updated data has been written to 'desc.json'.")

