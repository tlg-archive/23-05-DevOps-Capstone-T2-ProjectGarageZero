import json

# Load data from JSON files
with open('locations.json', 'r') as f:
    locations_data = json.load(f)

with open('items.json', 'r') as f:
    items_data = json.load(f)

# Define your classes here
class Location:
    def __init__(self, name, description, directions, items):
        self.name = name
        self.description = description
        self.directions = directions
        self.items = items

class Item:
    def __init__(self, name, description, location, use, item_type):
        self.name = name
        self.description = description
        self.location = location
        self.use = use
        self.item_type = item_type

# Define your functions for game logic here

# Create instances of your classes based on the loaded data
locations = []
for loc_data in locations_data['Locations']:
    # Check if 'Items' key exists in loc_data
    if 'Items' in loc_data:
        items = loc_data['Items']
    else:
        items = []  # If 'Items' key is missing, initialize it as an empty list
    location = Location(
        loc_data['Name'],
        loc_data['DescriptionID'],
        loc_data['Directions'],
        items  # Use the items list
    )
    locations.append(location)

items = []
for item_data in items_data['Items']:
    item = Item(
        item_data['Name'],
        item_data['DescriptionID'],
        item_data['Location'],
        item_data['Use'],
        item_data['Type']
    )
    items.append(item)

#ticket 89
# Implement your game logic and text parser here


# Example game loop
if __name__ == '__main__':
    while True:
        user_input = input("Enter your command: ")
        # Implement your text parser to process user commands
        # Check if the user wants to quit and break the loop if needed
        if user_input.lower() == "quit":
            print("Thanks for playing!")
            break
        else:
            # Process other user commands based on game logic
            # You can access the player's location, items, and more
            pass

# ticket 89 end

