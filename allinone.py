import json
import os
import sys

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
        location_head = f"LOCATION: {current_location}"

        # Print current # of moves made, increment up for the next loop -- CHANGE TO COUNTDOWN EVENTUALLY
        move_head = f"MOVES MADE: {counter}"

        counter += 1

        # Printing header
        print(f"{location_head : <25} {move_head : >25}\n")

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
        user_input = input("What would you like to do next? (type 'help' to see valid commands or 'quit' to exit):\n").strip().lower()

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
            print("\n-------------HELP SCREEN-------------")
            print("At any point throughout this game, you can:")
            print("-type 'inventory' to see your inventory")
            print("-type 'map' to see a map of the game")
            print("_____________________________________")
            print("\nValid Commands:")            
            print("type 'go' followed by a direction to to move")
            print("type 'quit' to exit the game")
            print("type 'get' followed by an item to retrieve the item")
            print("type 'drop' followed by an item to drop the item")
            print("\nCommands Coming Soon:")
            print("'talk' will allow you to talk to the characters")
            print("_____________________________________")
            print("\nGame Layout:")
            print(f"Current Location: Displayed in the top left")
            print(f"Moves you've taken: Displayed below")
            print(f"Description of your location: You will see the description of your current location")
            print("Your nearest exits: The places you can move to")
            print("_____________________________________")
            #added this to check for the return command
            print("\nType 'return' to return to the game.")
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
            print("\nType 'return' to return to the game.")
            while True:
                return_input = input("\n> ").strip().lower()
                if return_input == 'return':
                    clear_screen()
                    break
                else:
                    print("Invalid input. Type 'return' to return to the game.")
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
    #SAMMY: IMPORTING SYS FOR SYS.EXIT() TO QUIT
    import sys
    #SAMMY: CHANGING SO ONLY FUNCTION IMPORTED
    from functionsTest import start_game
    #from functionsTest import *

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_splash_screen():
        clear_screen()
        print("============================================")
        print("          Project Garage Zero:               ")
        print("       The Apprentice's Dilemma             ")
        print("============================================")
        input("Press Enter to continue...")
        clear_screen()

        print("Story:")
        print("\nYou are trying to become an apprentice for MSM and you have just left your interview.")
        print("But there's one problem: you can't remember where you parked your car!")
        print("You have a validated ticket but there's limited time before you have to pay extra for parking.")
        input("Press Enter to continue...")
        clear_screen()

        print("Objective:")
        print("\nBefore the step counter runs out, you need to find your car and leave the garage.")
        print("Face different obstacles on your quest to exit and avoid paying the additional parking fee.")
        input("Press Enter to continue...")
        clear_screen()

        print("Player:")
        print("\nYou are a young, bright-eyed individual, striving to become the next DevOps Engineer at MSM.")
        input("Press Enter to continue...")
        clear_screen()

        print("How to Win:")
        print("\nReach the garage exit and locate your car before the step counter runs out.")
        input("Press Enter to continue...")
        clear_screen()

        input("Press Enter to start a New Game...")

    def main_game_loop():
        #display_splash_screen()
        while True:
            clear_screen()
            print("Welcome to Project Garage Zero: The Apprentice's Dilemma!")
            print("1. Start a New Game")
            print("2. Quit")
            choice = input("> ")
            if choice == '1':
                # SAMMY: CALLING FUNCTION I MADE FROM FUNCTIONSTEST
                start_game()
            elif choice == '2':
                clear_screen()
                print("Goodbye!\n")
                sys.exit()
            else:
                input("Invalid choice. Press Enter to continue...")

    if __name__ == "__main__":
        main_game_loop()


