import json
from mapidea import display_map
import os
import pygame
from pygame import mixer # for music and SFX
import datetime

## LOADING JSON ##

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

## INITIAL GAME STATE ##

# Set initial inventory
inventory = []
# Initialize empty lists for storing previous commands and locations
previous_commands = []
previous_locations = []
# Set initial location
current_location= 'Elevator'
# Set initial counter
counter = 0

## FUNCTIONS ##

# Function to clear the screen (you can define this function if not already defined)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display player's inventory
def display_inventory():
    print("Inventory:")
    for item in inventory:
        print(item)
        
def press_enter_to_return():
    print("\nPress Enter to return to the game.")
    while True:
        return_input = input("\n> ").strip().lower()
        if return_input == '':
            clear_screen()
            break
        else:
            print("Invalid input. Press Enter to return to the game.")

# Save game functionality
def save_game():
        global current_location, counter, inventory, previous_commands, previous_locations, current_music_volume, current_sfx_volume
        save_data = {
        "current_location": current_location,
        "counter": counter,
        "inventory": inventory,
        "items_data": items_data,
        "previous_commands": previous_commands,
        "previous_locations": previous_locations,
        "current_music_volume": current_music_volume,
        "current_sfx_volume": current_sfx_volume
    }
        timestamp = datetime.datetime.now().strftime('%m-%d_%H-%M')
        with open(f'save_{timestamp}.json', 'w') as save_file:
            json.dump(save_data, save_file, indent=4)
            print(f"Game saved as save_{timestamp}.json!")

#verbs:
go = ["go", "move", "travel", "proceed", "journey", "advance"]
get = ["take", "get", "grab", "obtain", "acquire", "fetch", "procure", "attain"]
look = ["gaze", "stare", "observe", "peer", "examine"]
use = ["utilize", "employ", "apply", "utilise", "exploit"]
drop = ["drop", "leave", "discard", "abandon", "dump", "release"]
drive = ["drive", "navigate", "steer", "pilot", "operate", "motor"]
exit = ["exit", "leave", "depart", "vacate", "quit", "withdraw"]
start = ["start", "initiate", "commence", "launch", "begin", "ignite"]
talk = ["converse with", "communicate with", "speak to", "engage with", "interact with"]

## MUSIC AND SFX ##
# Setting current music volume value
current_music_volume=.3
# Setting current SFX volume value
current_sfx_volume = 0.7

# Function to set up and play background music
def background_music():
    pygame.init()
    pygame.mixer.init()
    s = 'sound'  # folder for music and FX
    music = pygame.mixer.Sound(os.path.join(s, 'garage_music.ogg'))
    pygame.mixer.music.load(os.path.join(s, 'garage_music.ogg'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(current_music_volume)

# Function to stop background music
def stop_background_music():
    pygame.mixer.music.stop()

# Functions to alter music volume
def volume_up():
    global current_music_volume
    current_music_volume += 0.1 
    pygame.mixer.music.set_volume(current_music_volume)
    
def volume_down():
    global current_music_volume
    current_music_volume -= 0.1
    pygame.mixer.music.set_volume(current_music_volume)

# Function to set up SFX channels
def setup_sfx():
    pygame.mixer.set_num_channels(8)  

# Function to start / stop SFX
def sfx_on():
    pygame.mixer.Channel(0).set_volume(current_sfx_volume)

def sfx_off():
    pygame.mixer.Channel(0).set_volume(0.0)

# Function to alter SFX volume
def sfx_volume_up():
    global current_sfx_volume
    current_sfx_volume += 0.1
    pygame.mixer.Channel(0).set_volume(current_sfx_volume)

def sfx_volume_down():
    global current_sfx_volume
    current_sfx_volume -= 0.1
    pygame.mixer.Channel(0).set_volume(current_sfx_volume)

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

## START GAME ##
# start game function defined but not auto-run when file imports
def start_game():
    #global variables
    global current_location, counter

    #Play background music and set up SFX
    background_music()
    setup_sfx()

    # Set initial location
    current_location = 'Elevator'
    # Set initial counter -- CHANGE TO COUNTDOWN EVENTUALLY
    counter = 0
 
    while True:
        # Print the current location
        location_head = f"LOCATION: {current_location}"

        # Print current # of moves made, increment up for next loop -- CHANGE TO COUNTDOWN EVENTUALLY
        move_head = f"MOVES MADE: {counter}"

        counter += 1

        # Printing header
        print(f"\n\n{location_head : <25} {move_head : >25}\n")

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

        # Add the user input to the commands list
        previous_commands.append(user_input)

        # Add the current location to the locations list
        previous_locations.append(current_location)

        # Check if the user wants to quit
        if user_input == 'quit':
            print("Exiting the game. Goodbye!")
            break

        # Check if user want to save game
        if user_input == "save":
            save_game()
            continue

        # Check if the user wants to stop music
        if user_input == 'musicoff':
            stop_background_music()

        # Check if the user wants to start music
        if user_input == 'musicon':
            background_music()

        # Check if the user wants to increase music volume
        if user_input == 'musicup':
            volume_up()
            print(f"Your music volume is now {int(current_music_volume * 10)} of 10")

        # Check if the user wants to decrease music volume
        if user_input == 'musicdown':
            volume_down()
            print(f"Your music volume is now {int(current_music_volume * 10)} of 10")
        
        # Check if the user wants to stop SFX
        if user_input == 'sfxoff':
            sfx_off()

        # Check if the user wants to start SFX
        if user_input == 'sfxon':
            sfx_on()

        # Check if the user wants to increase SFX volume
        if user_input == 'sfxup':
            sfx_volume_up()
            print(f"Your sound effects volume is now {int(current_sfx_volume * 10)} of 10")

        # Check if the user wants to decrease SFX volume
        if user_input == 'sfxdown':
            sfx_volume_down()
            print(f"Your sound effects volume is now {int(current_sfx_volume * 10)} of 10")

        # If the user wants to get an item
        if user_input.startswith('get '):
            # Get item name from the input
            item_to_get = user_input[4:]  # Remove "get " from the input

            # Check if the item is in the current room
            if item_to_get in available_items:
                # Call the get_item function to pick up the item
                get_item(item_to_get, current_location)
                # play a sound on channel 0 with a max time of 1250 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/get.mp3'), maxtime=1250)
            else:
                print("That's not here! (hint: type the name exactly)")

        # If the user wants to drop an item
        if user_input.startswith('drop '):
            # Get item name from the input
            item_to_drop = user_input[5:]  # Remove "drop " from the input
            # Call the drop_item function to drop the item
            drop_item(item_to_drop, current_location)
            # play a sound on channel 0 with a max time of 1000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=1000)

        if user_input == 'help':
            clear_screen()
            print("\n-------------HELP SCREEN-------------")
            print("At any point throughout this game, you can:")
            print("-type 'inventory' to see your inventory")
            print("-type 'map' to see a map of the game")
            print("_____________________________________")
            print("\nGame Layout:")
            print(f"Current Location: Displayed in the top left")
            print(f"Moves you've taken: Displayed below")
            print(f"Description of your location: You will see the description of your current location")
            print("Your nearest exits: The places you can move to")
            print("_____________________________________")
            print("\nGame Commands:")            
            print("type 'drop' followed by an item to drop the item") 
            print("type 'get' followed by an item to retrieve the item")
            print("type 'go' followed by a direction to to move")
            print("type 'quit' to exit the game")
            print("\nCommands Coming Soon:")
            print("'talk' will allow you to talk to the characters")
            print("_____________________________________")
            print("\nSound Commands:")
            print("type 'musicon' or 'musicoff' to toggle music")
            print("type 'musicup' or 'musicdown' to adjust music volume")
            print("type 'sfxon' or 'sfxoff' to toggle sound effects")
            print("type 'sfxup' or 'sfxdown' to adjust sound effects volume")
            print("_____________________________________")
            #added this to check for the return command
            # play a sound on channel 0 with a max time of 2000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/help.mp3'), maxtime=2000)
            press_enter_to_return()

            continue

        elif user_input == 'inventory':
            clear_screen()
            display_inventory()
            # play a sound on channel 0 with a max time of 1000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/inventory.mp3'), maxtime=1000) 
            press_enter_to_return()
        
        # Check if the user requests the map directly
        elif user_input == 'map':
            clear_screen()
            display_map()
            # play a sound on channel 0 with a max time of 1000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/map.mp3'), maxtime=1000)
            press_enter_to_return()
            continue

# Check if the user wants to display command and location history
        if user_input == 'history':
            clear_screen()
            print("History:")
            for i in range(min(len(previous_locations), len(previous_commands))):
                print(f"You used the '{previous_commands[i]}' command in the '{previous_locations[i]}'")
            press_enter_to_return()

        # Split the user input into words
        words = user_input.split()

        if len(words) < 2:
            print("Please include both a verb and a direction (e.g., 'go north').")
            continue

        verb, direction = words[0], " ".join(words[1:])

        # Check if the entered direction is valid
        valid_direction = False

        # Check if the user input matches "go" or its synonyms
        if any(user_input.startswith(verb) for verb in go):
            # Treat it as a "go" command
            verb = "go"


        for direction_data in available_directions:
            if direction == direction_data['Direction'].lower() and verb == 'go':
                current_location = direction_data['Destination']
                valid_direction = True
                # play a sound on channel 0 with a max time of 2000 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=2000)
                break

        if not valid_direction:
            print("Invalid direction. Please choose a valid direction.")

if __name__ == "__main__":
    start_game()
