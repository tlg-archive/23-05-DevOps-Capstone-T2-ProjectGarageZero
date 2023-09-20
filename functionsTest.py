import json
import os
import pygame
from pygame import mixer # for music and SFX
import pickle #for save games
from textwrap import wrap #to help limit description width
import shutil #dynamic line creation for section breaks
from interaction import get_npc, interact_with_npc, data

##################
## LOADING JSON ##
##################

# Load direction data from the JSON file
script_dir = os.path.dirname(os.path.realpath(__file__))
text_file = os.path.join(script_dir, 'data', 'game-text.json')
directions_file = os.path.join(script_dir, 'data', 'directions.json')

def convert_json():
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text
game_text = convert_json()

with open(directions_file, 'r') as f:
    directions_data = json.load(f)

# Load location data from the JSON file
locations_file = os.path.join(script_dir, 'data', 'locations.json')

with open(locations_file, 'r') as f:
    locations_data = json.load(f)

# Load description data from the JSON file
descriptions_file = os.path.join(script_dir, 'data', 'descriptions.json')

with open(descriptions_file, 'r') as f:
    descriptions_data = json.load(f)

# Load items data from the JSON file
items_file = os.path.join(script_dir, 'data', 'items.json')

with open(items_file, 'r') as f:
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

inside_mazda = False

# Updated map_visual with items in each SECTION
map_visual = [
    "Elevator [E]",
    "   |",
    "   |",
    "   V",
    "Parking West 1 [PW1] <--- > Parking East 1 [PE1]",
    "   ^                         ^",
    "   |                         |",
    "   V                         V",
    "Parking West 2 [PW2] <--- > Parking East 2 [PE2]",
    "   ^                         ^",
    "   |                         |",
    "   V                         V",
    "Parking West 3 [PW3] <--- > Parking East 3 [PE3]",
    "                                  ^",
    "                                  |",
    "                                  V",
    "                               Exit [X]"
]

# Dictionary to store items in each section
section_items = {
    "elevator": ["Garbage can", "Pack of gum"],
    "parking_west_1": [],
    "parking_west_2": ["Mazda", "Mouse"],
    "parking_west_3": [],
    "parking_east_1": ["Tesla", "Puddle", "Light"],
    "parking_east_2": ["Creepy Man", "Lollipop", "Newspaper"],
    "parking_east_3": [],
    "exit": ["Attendant"]
}

# Dictionary to store descriptions for items, locations, and NPCs
descriptions = {
    "Garbage can": "A greyidh greem garabage can placed near the elevstor, it id only hlaf full but mostly filled with reciepts.",
    "Pack of gum": "A black snf blue metsllic psck of gum rest on the floor prctically new and untouched.",
    "Mazda": "A dark grey Mazda CX-3 clearly in need of a good wash.",
    "Mouse": "A small brown mouse is perched ontop of the side mirror stopping you from entering the car.",
    "Tesla": "A blue tesla psrked nicely in its own spot slowly being consumed by the puddle next to it.",
    "Puddle": "A puddle slowly growing in size from a leaking pipe. With every drop of water from the leak the puddle consumes more of the parking area.",
    "Light": "A bright light fixture over the parking area reflexing off the puddle and the tesla, the light highlighting what you can afford one day if you are successful at this apprenticeship",
    "Creepy Man": "He wore a long, worn leather jacket that reached down to his ankles, and a wide-brimmed hat pulled low, obscuring most of his face. The shadow cast by his hat concealed his eyes, adding an air of mystery and unease..",
    "Lollipop": "The loolipop has a bright yellow ans pink wrapping, you cannot tell the flavor based purely on the wrapper.",
    "Newspaper": "A newspaper has smeared ink, you cannot tell how old the paper is. It is clearly just garbage.",
    "Attendant": "A young women sitting in a parking booth was scrolling on her phone to pass the time as she waits for people to leave the parking lot."
}



###############
## FUNCTIONS ##
###############

# Function to clear the screen (you can define this function if not already defined)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display player's inventory
def display_inventory():
    print("Inventory:")
    for item in inventory:
        print(item)


#DELETE LATER MAYBE       
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
    game_state = {
        "current_location": current_location,
        "counter": counter,
        "inventory": inventory,
        "items_data": items_data,
        "previous_commands": previous_commands,
        "previous_locations": previous_locations,
        "current_music_volume": current_music_volume,
        "current_sfx_volume": current_sfx_volume
    }
    
    with open('saved_game.pkl', 'wb') as file:
        pickle.dump(game_state, file)

    print("Game saved!")

# Load game functionality
def load_game():
    global current_location, counter, inventory, items_data, previous_commands, previous_locations, current_music_volume, current_sfx_volume
  
    try:
        with open('saved_game.pkl', 'rb') as file:
            game_state = pickle.load(file)

        current_location = game_state['current_location']
        counter = game_state['counter']
        inventory = game_state['inventory']
        items_data = game_state['items_data']
        previous_commands = game_state['previous_commands']
        previous_locations = game_state['previous_locations']
        current_music_volume = game_state['current_music_volume']
        current_sfx_volume = game_state['current_sfx_volume']

        print("Game successfully loaded!")
    except FileNotFoundError:
        print("No saved game found!")

###################
###Map Functions###
###################

# Function to display the map
def display_map():
    print("Map:")
    for line in map_visual:
        print(line)

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
    
    current_section = None
    for section, symbol in location_symbols.items():
        if symbol in current_location:
            current_section = section
            break
    
    for line in map_visual:
        if location_symbols[current_location] in line:
            print(">" + line)
        elif current_section and location_symbols[current_section] in line:
            item_list = section_items[current_section]
            if item_list:
                items = ", ".join(item_list)
                print(" " + line + f" ({items})")
            else:
                print(" " + line)
        else:
            print(" " + line)

def display_map_with_position(current_location):
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
    
    for line in map_visual:
        if location_symbols.get(current_location, "") in line:
            print(">" + line)
        else:
            print(" " + line)

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

#verbs:
go = ["go", "move", "travel", "proceed", "journey", "advance"]
get = ["take", "get", "grab", "obtain", "acquire", "fetch", "procure", "attain"]
look = ["look at", "gaze at", "stare at", "observe", "peer at", "examine", "look"]
drop = ["drop", "leave", "discard", "abandon", "dump", "release"]
exit = ["exit", "leave", "depart", "get out of"]
start = ["start", "turn on", "ignite"]
talk = ["converse with", "communicate with", "speak to", "engage with", "interact with", "talk to"]
enter = ["enter", "get inside", "get in", "sit in", "use"]

###################
## MUSIC AND SFX ##
###################

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

def look_at_item(item_name, current_location):
    # Check if the item is in the current location
    for item_data in items_data['Items']:
        if item_data['Name'].lower() == item_name and item_data['Location'] == current_location:
            print(item_data['Description'])
            return
    print("That item is not here or cannot be examined.")

################
## START GAME ##
################

# start game function defined but not auto-run when file imports
def start_game():
    #global variables
    global current_location, counter, car_started

    car_started = False


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

        #counter += 1

        # Printing header
        print(f"\n{location_head : <25} {move_head : >25}\n")

        # Get and print the current location's description
        current_location_data = None
        for location in locations_data['Locations']:
            if location['Name'] == current_location:
                current_location_data = location
                break

        if current_location_data:
            wrapped_description = wrap(current_location_data['Description'], width=60)
            for line in wrapped_description:
                print(line)
            print("\n") 

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
        user_input = input("What would you like to do next? (type 'help' to see valid commands or 'quit' to exit): \n>> ").strip().lower()

        # Check if user wants to load a saved game
        if user_input == 'load':
            load_game()
            continue

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
        if any(user_input.startswith(verb) for verb in get):
            # Get item name from the input
            item_to_get = user_input.split(maxsplit=1)[1]  # Remove the verb from the input

            # Check if the item is in the current room
            if item_to_get in available_items:
                # Call the get_item function to pick up the item
                get_item(item_to_get, current_location)
                # play a sound on channel 0 with a max time of 1250 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/get.mp3'), maxtime=1250)
            else:
                print("That's not here! (hint: type the name exactly)")

        # If the user wants to drop an item
        if any(user_input.startswith(verb) for verb in drop):
            # Get item name from the input
            item_to_drop = user_input.split(maxsplit=1)[1]  # Remove "drop " from the input
            # Call the drop_item function to drop the item
            drop_item(item_to_drop, current_location)
            # play a sound on channel 0 with a max time of 1000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=1000)

        if user_input == 'help':
            #clear_screen()
            print(game_text['help'])
            #added this to check for the return command
            # play a sound on channel 0 with a max time of 2000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/help.mp3'), maxtime=2000)
            #press_enter_to_return()

            continue

        elif user_input == 'inventory':
            #clear_screen()
            display_inventory()
            # play a sound on channel 0 with a max time of 1000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/inventory.mp3'), maxtime=1000) 
            #press_enter_to_return()
        
        # Check if the user requests the map directly
        elif user_input == 'map':
            #clear_screen()
            display_map()
            # play a sound on channel 0 with a max time of 1000 milliseconds
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/map.mp3'), maxtime=1000)
            #press_enter_to_return()
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

        if any(user_input.startswith(verb) for verb in look):
            verb = "look at"

        if verb == 'look at':
            # Get item name from the input
            item_to_look_at = " ".join(words[2:])  # Remove the "look at" part from the input
            # Call the look_at_item function to show the item's description
            look_at_item(item_to_look_at, current_location)

        if user_input.startswith('talk'):
            npc_name = user_input.split(maxsplit=1)[1]  
            npc = get_npc(npc_name)  
            if npc:
                interact_with_npc(npc)  
            else:
                print(f"No NPC named {npc_name} found.")
            continue 

###############################
##############mazda############
##############################
        # If the user wants to get an item
        if any(user_input.startswith(verb) for verb in enter):
            # Get item name from the input
            item_to_get = user_input.split(maxsplit=1)[1]  # Remove the verb from the input

            # Check if the item is the "mazda"
            if item_to_get.lower() == 'mazda':
                # Check if the player is already in the "mazda"
                if current_location == 'Parking West 2' and 'mazda' not in inventory:
                    # Add the "mazda" to the inventory
                    inventory.append('mazda')
                    # play a sound on channel 0 with a max time of 1500 milliseconds
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
                    press_enter_to_return()
                    print("You have entered the Mazda.")
                    continue
                elif 'mazda' in inventory:
                    print("You are already in the Mazda.")
                    continue

            # Check if the item is in the current room
            if item_to_get in available_items:
                # Call the get_item function to pick up the item
                get_item(item_to_get, current_location)
                # play a sound on channel 0 with a max time of 1250 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/get.mp3'), maxtime=1250)
            else:
                print("That's not here! (hint: type the name exactly)")

        if 'mazda' in inventory:
            # Check if the user wants to start the car
            if any(user_input.startswith(verb) for verb in start):
                # Add a flag to indicate that the car has been started
                car_started = True
                # play a sound on channel 0 with a max time of 50000 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/carstart.mp3'), maxtime=5000)
                press_enter_to_return()
                print("You have started the car.")
                continue
            
            # Check if the car has been started before allowing "go" command
            if not car_started:
                print("You need to start the car before you can go anywhere.")
                continue


        # If the user wants to exit
        if any(user_input.startswith(verb) for verb in exit):
            # Check if the player is in the Mazda
            if 'mazda' in inventory:
                # Remove the Mazda from the inventory
                inventory.remove('mazda')
                # play a sound on channel 0 with a max time of 1500 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
                press_enter_to_return()
                print("You have exited the Mazda.")
            else:
                print("You are not inside the Mazda.")
            continue

###############################
##############mazda############
##############################

        for direction_data in available_directions:
            if direction == direction_data['Direction'].lower() and verb == 'go':
                current_location = direction_data['Destination']
                valid_direction = True
                counter += 1
                # play a sound on channel 0 with a max time of 2000 milliseconds
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=2000)
                break

        if not valid_direction:
            print("Invalid direction. Please choose a valid direction.")

        terminal_width, _ = shutil.get_terminal_size()
        print("-" * terminal_width)


if __name__ == "__main__":
    display_map_with_items("elevator")
    # Test the "Look" command
    look_command("Look Garbage can")
    look_command("Look Tesla")
    look_command("Look Nonexistent Item")    
    start_game()
