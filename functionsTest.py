import json
from mapidea import display_map
import os

# Function to clear the screen (you can define this function if not already defined)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Load direction data from the JSON file
with open('directions.json', 'r') as f:
    directions_data = json.load(f)

# Load location data from the JSON file
with open('locations.json', 'r') as f:
    locations_data = json.load(f)

# Load description data from the JSON file
with open('descriptions.json', 'r') as f:
    descriptions_data = json.load(f)

# Load items data from the JSON file
with open('items.json', 'r') as f:
    items_data = json.load(f)

# Set initial inventory
inventory = []

# Function to display player's inventory
def display_inventory():
    print("Inventory:")
    for item in inventory:
        print(item)

# Get item
def get_item(item_name, current_location):
    # Check if the item is in the current location
    for item_data in items_data['Items']:
        if item_data['Name'].lower() == item_name and item_data['Location'] == current_location:
            inventory.append(item_data['Name'])
            # Remove the item from the current location
            items_data['Items'].remove(item_data)
            print(f"You now have {item_data['Name']}.")
            return
    print("That's not here! (hint: type name exactly!)")

# Drop item
def drop_item(item_name, current_location):
    # Check if the item is in the player's inventory
    if item_name in inventory:
        # Dictionary for item data
        item_to_drop = {
            "Name": item_name,
            "Location": current_location,
            "Use": "none",
            "Type": "none",
            "Note": "none",
            "Description": f"A {item_name} on the ground."
        }

        # Add the item to the current location's items
        items_data['Items'].append(item_to_drop)
        # Remove the item from the player's inventory
        inventory.remove(item_name)
        print(f"You dropped {item_name}.")
    else:
        print("You don't have that on you!")


# start game function defined but not auto-run when file imports
def start_game():

    # Set initial location
    current_location = 'Elevator'
    # Set initial counter -- CHANGE TO COUNTDOWN EVENTUALLY
    counter = 0
 
    while True:
        # Print the current location
        print(f"LOCATION: {current_location}")

        # Print current # of moves made, increment up for next loop -- CHANGE TO COUNTDOWN EVENTUALLY
        print(f"MOVES MADE: {counter}\n")
        counter += 1

        # Get and print the current location's description
        current_location_data = None
        for location in locations_data['Locations']:
            if location['Name'] == current_location:
                current_location_data = location
                break

        if current_location_data:
            print(f"{current_location_data['Description']}\n") 

        # Get items in room
        available_items = []
        for item_data in items_data['Items']:
            if item_data['Location'] == current_location:
                available_items.append(item_data['Name'])

        # List items
        if available_items:
            print("ITEMS:")
            for item in available_items:
                print(item)

        # Print the available directions
        print(f"\nEXITS:")
        available_directions = []
        for location_data in directions_data['Directions']:
            if location_data['Location'] == current_location:
                available_directions = location_data['Directions']
                break

        for direction_data in available_directions:
            print(f"{direction_data['Direction']} - {direction_data['Destination']}\n")

        # Get user input for the direction
        user_input = input("Enter a direction to move (e.g., 'go north') or 'quit' to exit:\n").strip().lower()

        # Check if the user wants to quit
        if user_input == 'quit':
            print("Exiting the game. Goodbye!")
            break

        # If the user wants to get an item
        if user_input.startswith('get '):
            # Get item name from the input
            item_to_get = user_input[4:]  # Remove "get " from the input

            # Check if the item is in the current room
            if item_to_get in available_items:
                # Call the get_item function to pick up the item
                get_item(item_to_get, current_location)
            else:
                print("That's not here! (hint: type the name exactly)")

        # If the user wants to drop an item
        if user_input.startswith('drop '):
            # Get item name from the input
            item_to_drop = user_input[5:]  # Remove "drop " from the input
            # Call the drop_item function to drop the item
            drop_item(item_to_drop, current_location)

        if user_input == 'help':
            clear_screen()
            print("\n___________HELP SCREEN___________")
            print("\nTo move, type a valid command. For example, 'go south' will move you one place south.")
            print("Game Layout")
            print("_____________________________________")
            print(f"Current Location: Displayed in the top left")
            print(f"Moves you've taken: Displayed below")
            print(f"Description of your location: You will see the description of your current location")
            print("Your nearest exits: The places you can move to")
            print("_____________________________________")
            print("Below is a map of the game:")
            display_map()  # Call the display_map() function to show the map
            #added this to check for the return command
            print("\nType 'return' to return to the game loop.")
            while True:
                return_input = input("\n> ").strip().lower()
                if return_input == 'return':
                    clear_screen()
                    break
                else:
                    print("Invalid input. Type 'return' to return to the game loop.")

            continue
        
        elif user_input == 'inventory':
            clear_screen()
            display_inventory() 
            print("\nType 'return' to return to the game.")
            while True:
                return_input = input("\n> ").strip().lower()
                if return_input == 'return':
                    clear_screen()
                    break
                else:
                    print("Invalid input. Type 'return' to return to the game loop.")
        
        # Check if the user requests the map directly
        elif user_input == 'map':
            clear_screen()
            display_map()
            continue

        # Split the user input into words
        words = user_input.split()

        if len(words) < 2:
            print("Please include both a verb and a direction (e.g., 'go north').")
            continue

        verb, direction = words[0], " ".join(words[1:])

        # Check if the entered direction is valid
        valid_direction = False
        for direction_data in available_directions:
            if direction == direction_data['Direction'].lower() and verb == 'go':
                current_location = direction_data['Destination']
                valid_direction = True
                break

        if not valid_direction:
            print("Invalid direction. Please choose a valid direction.")

if __name__ == "__main__":
    start_game()
