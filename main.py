import json

#This script defines classes for locations, items, characters, and verbs and loads data from the respective JSON files. 

# Load data from JSON files
with open('locations.json', 'r') as f:
    locations_data = json.load(f)

with open('items.json', 'r') as f:
    items_data = json.load(f)

with open('characters.json', 'r') as f:
    characters_data = json.load(f)

with open('verbs.json', 'r') as f:
    verbs_data = json.load(f)

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

class Character:
    def __init__(self, name, character_type, alignment, change_alignment, quotes):
        self.name = name
        self.character_type = character_type
        self.alignment = alignment
        self.change_alignment = change_alignment
        self.quotes = quotes

class Verb:
    def __init__(self, name):
        self.name = name

##It then creates instances of these classes based on the data and provides an example of how to access and print information about these game elements. 

# Create Location instances
locations = []
for loc_data in locations_data['Locations']:
    location = Location(loc_data['Name'], loc_data['Description'], loc_data['Directions'], loc_data['Items'])
    locations.append(location)

# Create Item instances
items = []
for item_data in items_data['Items']:
    item = Item(item_data['Name'], item_data['Description'], item_data['Location'], item_data['Use'], item_data['Type'])
    items.append(item)

# Create Character instances
characters = []
for char_data in characters_data:
    character = Character(char_data['Name'], char_data['Type'], char_data['Align'], char_data['ChangeAlign'], char_data['Quote'])
    characters.append(character)

# Create Verb instances
verbs = [Verb(verb) for verb in verbs_data]



# Example usage
if __name__ == '__main__':
    # Accessing and printing information about locations, items, characters, and verbs
    for location in locations:
        print(f"Location: {location.name}")
        print(f"Description: {location.description}")
        print(f"Directions: {location.directions}")
        print(f"Items: {location.items}")
        print("\n")

    for item in items:
        print(f"Item: {item.name}")
        print(f"Description: {item.description}")
        print(f"Location: {item.location}")
        print(f"Use: {item.use}")
        print(f"Type: {item.item_type}")
        print("\n")

    for character in characters:
        print(f"Character: {character.name}")
        print(f"Type: {character.character_type}")
        print(f"Alignment: {character.alignment}")
        print(f"Change Alignment: {character.change_alignment}")
        print(f"Quotes: {character.quotes}")
        print("\n")

    for verb in verbs:
        print(f"Verb: {verb.name}")



########tix 89 below: 

# Load your game data (locations, items, characters, verbs) from JSON files

# Define a list of valid verbs from your verbs.json file
valid_verbs = ["get", "go", "drive", "exit", "give", "help", "ignore", "inventory", "look", "open", "pull", "put", "start", "talk", "time", "use"]

# Get user input
user_input = input("Enter your command: ")
words = user_input.lower().split()  # Convert to lowercase and split

# Parse the input
if len(words) >= 2:
    verb, noun = words[0], words[1]
    # Check if the verb is valid
    if verb in valid_verbs:
        # Match and execute actions based on the verb and noun
        if verb == "go":
            # Handle "go" command
            # Check if the noun (location) is valid and accessible from the current location
            # Update the player's location
            pass  # Placeholder for handling "go" command
        elif verb == "get":
            # Handle "get" command (pick up items)
            # Check if the noun (



#########################tix 89 done. ##################
