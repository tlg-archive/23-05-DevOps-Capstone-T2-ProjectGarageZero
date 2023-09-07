import json
from ticket_83 import *

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

# Create instances of your classes based on the loaded data
locations = []
for loc_data in locations_data['Locations']:
    if 'Items' in loc_data:
        items = loc_data['Items']
    else:
        items = []  
    location = Location(
        loc_data['Name'],
        loc_data['DescriptionID'],
        loc_data['Directions'],
        items
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

# Dictionary to store descriptions for items, locations, and NPCs
descriptions = {
    "Garbage can": "A greyidh greem garabage can placed near the elevstor, it id only hlaf full but mostly filled with reciepts.",
    "Pack of gum": "A black snf blue metsllic psck of gum rest on the floor prctically new and untouched.",
    "Mazda": "A dark grey Mazda CX-3 clearly in need of a good wash.",
    "Mouse": "A small brown mouse is perched ontop of the side mirror stopping you from entering the car.",
    "Tesla": "A blue tesla psrked nicely in its own spot slowly being consumed by the puddle next to it.",
    "Puddle": "A puddle slowly growing in size from a leaking pipe. With every drop of water from the leak the puddle consumes more of the parking area.",
    "Light": "A bright light fixture over the parking area reflexing off the puddle and the tesla, the light highlighting what you can afford one day if you are successful at this apprenticeship",
    "Creepy Man": "He wore a long, worn leather jacket that reached down to his ankles, and a wide-brimmed hat pulled low, obscuring most of his face. The shadow cast by his hat concealed his eyes, adding an air of mystery and unease.",
    "Lollipop": "The loolipop has a bright yellow ans pink wrapping, you cannot tell the flavor based purely on the wrapper.",
    "Newspaper": "A newspaper has smeared ink, you cannot tell how old the paper is. It is clearly just garbage.",
    "Attendant": "A young women sitting in a parking booth was scrolling on her phone to pass the time as she waits for people to leave the parking lot."
}

# Function to look at an item, location, or NPC and display its description
def look_command(input_text):
    parts = input_text.split()
    
    if len(parts) < 2:
        print("Please specify what you want to look at.")
    else:
        item_name = " ".join(parts[1:])
        if item_name in descriptions:
            print(descriptions[item_name])
        else:
            print(f"You don't see {item_name} here.")

# Example function to display the map with items and the current location highlighted
def display_map_with_items(current_location):
    location_symbols = {
        "elevator": "[E]",
        "parking_west_1": "[PW1]",
        "parking_west_2": "[PW2]",
        "parking_west_3": "[PW3]",
        "parking_east_1": "[PE1]",
        "parking_east_2": "[PE2]",
        "parking_east_3": "[PE3]",
        "exit": "[X]"
    }
    
    # Simple display implementation
    for location, symbol in location_symbols.items():
        if location == current_location:
            print(f"{symbol} <-- You are here!")
        else:
            print(symbol)

# Main game loop
if __name__ == '__main__':
    display_splash_screen()
    new_game()
    current_location = "elevator"  # This is just for the example; change this based on your game's initial state
    
    while True:
        user_input = input("Enter your command: ")
        
        if user_input.lower() == "quit":
            print("Thanks for playing!")
            break
        elif user_input.lower().startswith("look"):
            look_command(user_input)
        elif user_input.lower().startswith("map"):
            display_map_with_items(current_location)
        else:
            main_game_loop()

