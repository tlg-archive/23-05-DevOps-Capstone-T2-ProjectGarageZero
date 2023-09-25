import json
import os
import pygame
from pygame import mixer # for music and SFX
import pickle #for save games
from textwrap import wrap #to help limit description width
import shutil #dynamic line creation for section breaks
from interaction import get_npc, interact_with_npc, data
import random
import sys

#Suppressing Pygame support prompt that was displaying pre-splash screen
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
##################
## LOADING JSON ##
##################

# Load direction data from the JSON file
script_dir = os.path.dirname(os.path.realpath(__file__))
text_file = os.path.join(script_dir, 'data', 'game-text.json')

#LOAD BASIC GAME TEXT JSON
def convert_json():
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text
game_text = convert_json()

directions_file = os.path.join(script_dir, 'data', 'directions.json')

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

# Load NPC Data from JSON file
npcdata_file = os.path.join(script_dir, 'data', 'npcdata.json')
with open(npcdata_file, 'r') as file:
    npc_data = json.load(file)

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

###############
## FUNCTIONS ##
###############

# Function to clear the screen (you can define this function if not already defined)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
################
## GAME INFO ##
################
"""
SoundController CLASS HAS
- Background Music Settings
- SFX Sound Settings
"""

class SoundController:
    def __init__(self):
        # Setting current music volume value
        self.current_music_volume=.3
        # Setting current SFX volume value
        self.current_sfx_volume = 0.7

    def background_music():
        pygame.init()
        pygame.mixer.init()
        s = 'sound'  # folder for music and FX
        music = pygame.mixer.Sound(os.path.join(s, 'garage_music.ogg'))
        pygame.mixer.music.load(os.path.join(s, 'garage_music.ogg'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(current_music_volume)

    def stop_background_music():
        pygame.mixer.music.stop()

    def volume_up():
        global current_music_volume
        current_music_volume += 0.1 
        pygame.mixer.music.set_volume(current_music_volume)
    
    def volume_down():
        global current_music_volume
        current_music_volume -= 0.1
        pygame.mixer.music.set_volume(current_music_volume)

    def setup_sfx():
        pygame.mixer.set_num_channels(8) 

    def sfx_on():
        pygame.mixer.Channel(0).set_volume(current_sfx_volume)

    def sfx_off():
        pygame.mixer.Channel(0).set_volume(0.0)

    def sfx_volume_up():
        global current_sfx_volume
        current_sfx_volume += 0.1
        pygame.mixer.Channel(0).set_volume(current_sfx_volume)

    def sfx_volume_down():
        global current_sfx_volume
        current_sfx_volume -= 0.1
        pygame.mixer.Channel(0).set_volume(current_sfx_volume)


"""
Player CLASS HAS
- Inventory
- get item function
- drop item function
"""
class Player:
    def __init__(self):
        self.inventory = []
    
    def get_item(self, item_name):
        for item_data in items_data['Items']:
            if item_data['Name'].lower() == item_name and item_data['Location'] == new_game.current_location:
                self.inventory.append(item_data['Name'])
                # Remove the item from the current location
                items_data['Items'].remove(item_data)
                print(f"You now have {item_data['Name']}.")
                return
        print("That's not here! (hint: type name exactly!)")
    
    def drop_item(self, item_name, current_location):
        # Check if the item is in the player's inventory
        if item_name in self.inventory:
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
            self.inventory.remove(item_name)
            print(f"You dropped {item_name}.")
        else:
            print("You don't have that on you!")

"""
LocationData CLASS HAS
- Load location data
- Show Location Data
- Look at items in location data
"""
class LocationData:
    def __init__(self):
        self.current_location = ''
        self.current_location_data = {}
        self.available_directions = []
        self.available_items = []

    def load_location_data(self):
        #print(f"current location in load data: {new_game.current_location}\n\n")
        self.current_location = new_game.current_location
        for location in locations_data['Locations']:
            if location['Name'] == self.current_location:
                self.current_location_data = location
                break

        # Get items in room
        self.available_items = []
        for item_data in items_data['Items']:
            if item_data['Location'] == self.current_location:
                self.available_items.append(item_data['Name'])

        #available_directions = []
        #self.available_directions = self.current_location_data['Directions']
        for location_data in directions_data['Directions']:
            if location_data['Location'] == self.current_location:
                self.available_directions = location_data['Directions']
                break

    def show_location_data(self):
        new_game.location_data.load_location_data()
        location_head = f"LOCATION: {self.current_location}"
        # Print current # of moves made, increment up for next loop -- CHANGE TO COUNTDOWN EVENTUALLY
        move_head = f"MOVES LEFT: {new_game.counter}"
        print("------------------------------")
        print(f"\n{location_head : <25} {move_head : >25}\n")
        if self.current_location_data:
            wrapped_description = wrap(self.current_location_data['Description'], width=60)
            for line in wrapped_description:
                print(line)
            print("\n") 

        # List items
        if self.available_items:
            print("ITEMS:")
            for item in self.available_items:
                print(item)

        # Print the available directions
        print(f"\nEXITS:")
        for direction_data in self.available_directions:
            print(f"{direction_data['Direction']} - {direction_data['Destination']}\n")
        print("------------------------------")

    def look_at_item(self, noun):
        print(f'I LOOK AT {noun}')
        pass

"""
NPCData CLASS HAS
- NPC data
- get npc function
- greet npc function
- interact with npc function
"""
class NPCData:
    def __init__(self) -> None:
        pass
    
    def get_npc(self, npc_name):
        for npc in npc_data['NPCs']:
            if npc['Name'] == npc_name:
                return npc
        return None
    
    def greet_npc(self,npc):
        if 'Greetings' in npc:
            return random.choice(npc['Greetings'])
        return None

    def interact_with_npc(self, npc):
        print(self.greet_npc(npc))
        
        if 'PlayerChoices' in npc:
            while True:  # This loop allows the player to keep choosing until they decide to exit
                for idx, choice in enumerate(npc['PlayerChoices']):
                    print(f"{idx + 1}. {choice['Choice']}")

                # Add an option to exit the conversation
                exit_option_index = len(npc['PlayerChoices']) + 1
                print(f"{exit_option_index}. Exit conversation")

                player_choice = input("Choose an option (type the number): ")

                try:
                    choice_index = int(player_choice) - 1
                    if 0 <= choice_index < len(npc['PlayerChoices']):
                        if 'Response' in npc['PlayerChoices'][choice_index]:
                            response = npc['PlayerChoices'][choice_index]['Response']
                        elif 'ResponseOptions' in npc['PlayerChoices'][choice_index]:
                            response = random.choice(npc['PlayerChoices'][choice_index]['ResponseOptions'])
                        else:
                            response = "No response found."
                        print(response)
                    elif choice_index + 1 == exit_option_index:  # Exit conversation
                        print("Exiting conversation.")
                        return  # This returns the player to the main command input
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid choice.")

"""
TextParser CLASS HAS
- all multiple word command logic
"""
class TextParser:
    def parse_command(self, command):
        #global inventory
        command_words = command.split(' ')
        #print(command_words)
        verb = command_words[0]
        noun = ' '.join(command_words[1:]) if len(command_words) > 1 else None
        #print(f"verb {verb} noun {noun}")

        synonyms = {
            'go' : ["go", "move", "travel", "proceed", "journey", "advance"],
            'get' : ["take", "get", "grab", "obtain", "acquire", "fetch", "procure", "attain"],
            'look' : ["look at", "gaze at", "stare at", "observe", "peer at", "examine", "look"],
            'drop' : ["drop", "leave", "discard", "abandon", "dump", "release"],
            'exit' : ["exit", "leave", "depart", "get out of"],
            'start' : ["start", "turn on", "ignite"],
            'talk' : ["talk","ask", "communicate", "speak", "engage", "interact"],
            'enter' : ["enter", "get inside", "get in", "sit in", "use"]
        }
        
        for key, values in synonyms.items():
            if verb in values:
                method_name= f"handle_{key}"
                method = getattr(self, method_name, None)

                if method and callable(method):
                    method(noun)
                    return
        print(game_text["invalid"])
    
    def handle_go(self,noun):
        print(f'inventory: {new_game.player.inventory}')
        if 'mazda' in new_game.player.inventory:
            self.handle_go_mazda(noun)
        else:
            self.handle_go_norm(noun)
    
    def handle_go_norm(self, noun):
        print(f"Handling GO command for {noun}")
        direction = noun.title()
        #print(f"available directions: {new_game.location_data.available_directions}")
        if new_game.counter == 1:
            print("OH NO! Time is up and you did not leave the parking lot before you had to pay the extra parking fee. Try again and see if you can get your car and leave!")
            sys.exit()

        if direction in new_game.location_data.current_location_data['Directions']:
            if new_game.location_data.current_location_data['Directions'][direction] == "Elevator" and 'mazda' in new_game.player.inventory:
                print("You can't take the Mazda into the elevator!")
                return
            new_game.current_location = new_game.location_data.current_location_data['Directions'][direction]
            print(f"current location in handle go: {new_game.current_location}")
            # play a sound on channel 0 with a max time of 2000 milliseconds
            #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=2000)
            new_game.counter -= 1
        else:
            print(f"Invalid choice. You cannot go {noun} Try again")
    
    #UNCOMMENT SOUND COMMAND  
    def handle_start(self, noun):
        print(f"Handling START command for {noun}")
        if 'mazda' in new_game.player.inventory:
            if new_game.car_started == False:
                new_game.car_started = True
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/carstart.mp3'), maxtime=5000)
                print('You started car your car.')
            else:
                print('Your car is already started.')
        else:
            print("You can't start anything right now. Have you found your car yet?")

    #UNCOMMENT SOUND COMMAND
    def handle_enter(self, noun):
        print(f"Handling ENTER command for {noun}")
        if noun.lower() == 'mazda':
            if new_game.current_location == 'Parking West 2' and 'mazda' not in new_game.player.inventory:
                # Add the "mazda" to the inventory
                #new_game.player.inventory.append('mazda')
                new_game.player.get_item('mazda')
                # play a sound on channel 0 with a max time of 1500 milliseconds
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
                print("You have entered the Mazda.")
                return
            elif 'mazda' in new_game.player.inventory:
                print("You are already in the Mazda.")
                return
        else:
            print(f'You cannot enter {noun}')

    #UNCOMMENT SOUND COMMANDS
    #UPDATE THIS WHEN THE DROP ITEM COMMAND IS IMPLEMENTED
    def handle_exit(self, noun):
        print(f"Handling EXIT command for {noun}")
        if noun.lower() == 'mazda':
            if 'mazda' in new_game.player.inventory:
                # Remove the Mazda from the inventory
                new_game.player.inventory.remove('mazda')
                # play a sound on channel 0 with a max time of 1500 milliseconds
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
                print("You have exited the Mazda.")
            else:
                print("You are not inside the Mazda.")
        else:
            print(f'You cannot EXIT {noun}')

    def handle_go_mazda(self, noun):
        if new_game.car_started == False:
            print('Please START your MAZDA to in order to move to a new room.')
        else:
            self.handle_go_norm(noun)

    def handle_get(self, noun):
        print(f"Handling GET command for {noun}")
        new_game.player.get_item(noun)

    def handle_drop(self, noun):
        current_location = new_game.current_location
        new_game.player.drop_item(noun, current_location)

    def handle_look(self, noun):
        print(f"Handling LOOK command for {noun}")
        new_game.location_data.look_at_item(noun)

    def handle_talk(self, noun):
        npc_name = noun
        print(f"Handling TALK command for {noun}")
        npc = new_game.npcs.get_npc(npc_name)
        if npc:
            interact_with_npc(npc)
        else:
            print(f"No NPC named {npc_name} found.")

"""
GameCommand CLASS HAS
- Base input logic
- Show history function
- Display Map function
"""
class GameCommand:   
    def __init__(self):
        self.previous_commands = []
        self.previous_locations = []
        #USE THIS TO CALL THE SOUND CONTROLLER FUNCTIONS
        self.sound_settings = SoundController()

    def show_history(self):
        print("History:")
        for i in range(min(len(self.previous_locations), len(self.previous_commands))):
            print(f"You used the '{self.previous_commands[i]}' command in the '{self.previous_locations[i]}'")

    def display_map(self):
        print("Map:")
        for line in map_visual:
            print(line)

    def handle_input(self, command):
        if command in ['save']:
            new_game.save_game()
        elif command in ['load']:
            new_game.load_game() 
        elif command in ['musicon']:
            self.sound_settings.background_music()
        elif command in ['musicoff']:
            self.sound_settings.stop_background_music()
        elif command in ['musicup']:
            self.sound_settings.volume_up()
        elif command in ['musicdown']:
            self.sound_settings.volume_down()
        elif command in ['sfxon']:
            self.sound_settings.sfx_on()
        elif command in ['sfxoff']:
            self.sound_settings.sfx_off()
        elif command in ['sfxup']:
            self.sound_settings.sfx_volume_up()
        elif command in ['sfxdown']:
            self.sound_settings.sfx_volume_down()
        elif command in ['help']:
            pass
        elif command in ['inventory']:
            pass
        elif command in ['map']:
            self.display_map()
        elif command in ['history']:
            self.show_history()
        elif command in ['quit']:
            pass
        else:
            new_game.text_parser.parse_command(command)

"""
GameEngine CLASS HAS
- Create a player class
- track location data via LocationData class
- TextParser
- Step Counter
- Current Location tracker
- Inside Mazda flag
- Car Started flag
- Play Game function
- Save Game function
- Load Game function
"""
class GameEngine:
    def __init__(self):
        self.player = Player()
        self.location_data = LocationData()
        self.counter = 15 #SETS MAX NUMBER OF STEPS FOR THE GAME
        self.insideMazda = False
        self.car_started = False
        self.current_location = 'Elevator'
        self.commander = GameCommand()
        self.text_parser = TextParser()
        self.npcs = NPCData()

    def save_game(self):
        game_state = {
            "current_location": self.current_location,
            "counter": self.counter,
            "inventory": self.player.inventory,
            # Assuming you add items_data and volume settings to GameEngine or another class
            # "items_data": self.items_data,
            # "current_music_volume": self.sound_settings.current_music_volume,
            # "current_sfx_volume": self.sound_settings.current_sfx_volume,
            "previous_commands": self.commander.previous_commands,
            "previous_locations": self.commander.previous_locations
        }
        
        with open('saved_game.pkl', 'wb') as file:
            pickle.dump(game_state, file)

        print("Game saved!")

    def load_game(self):
        try:
            with open('saved_game.pkl', 'rb') as file:
                game_state = pickle.load(file)

            self.current_location = game_state['current_location']
            self.counter = game_state['counter']
            self.player.inventory = game_state['inventory']
            # Assuming you add items_data and volume settings to GameEngine or another class
            # self.items_data = game_state['items_data']
            # self.sound_settings.current_music_volume = game_state['current_music_volume']
            # self.sound_settings.current_sfx_volume = game_state['current_sfx_volume']
            self.commander.previous_commands = game_state['previous_commands']
            self.commander.previous_locations = game_state['previous_locations']

            print("Game successfully loaded!")
        except FileNotFoundError:
            print("No saved game found!")

    #ADD START BACKGROUND MUSIC AND SFX COMMAND WHEN THEY ARE BUILT IN
    def play_game(self):
        self.current_location = 'Elevator'
        #self.location_data.show_location_data()
        while True:
            self.location_data.show_location_data()
            user_input = input("What would you like to do next? (type 'help' to see valid commands or 'quit' to exit): \n>> ").strip().lower()
            self.commander.handle_input(user_input)

new_game = GameEngine()

if __name__ == "__main__":
    new_game.play_game()
