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
class SoundController:
    def __init__(self):
        # Setting current music volume value
        self.current_music_volume=.3
        # Setting current SFX volume value
        self.current_sfx_volume = 0.7

    def background_music():
        pass

    def stop_background_music():
        pass

    def volume_up():
        pass

    def volume_down():
        pass

    def setup_sfx():
        pass

    def sfx_on():
        pass

    def sfx_off():
        pass

    def sfx_volume_up():
        pass

    def sfx_volume_down():
        pass

class Player:
    def __init__(self):
        self.inventory = []
    def get_item():
        pass
    def drop_item():
        pass
    def look_at_item():
        pass

class LocationData:
    def __init__(self):
        self.current_location = ''
        self.current_location_data = {}
        self.available_directions = []
        self.available_items = []

    def load_location_data(self):
        print(f"current location in load data: {new_game.current_location}\n\n")
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
        move_head = f"MOVES MADE: {new_game.counter}"
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

class TextParser:
    def parse_command(self, command):
        #global inventory
        command_words = command.split(' ')
        print(command_words)
        verb = command_words[0]
        noun = ' '.join(command_words[1:]) if len(command_words) > 1 else None
        print(f"verb {verb} noun {noun}")

        """ if verb == 'save':
            self.save_game()
            print(game_text["save_game"])
            return

        if verb == 'load':
            self.load_game()
            print(game_text["load_game"])
            return """

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
        print(f"available directions: {new_game.location_data.available_directions}")
        if direction in new_game.location_data.current_location_data['Directions']:
            new_game.current_location = new_game.location_data.current_location_data['Directions'][direction]
            print(f"current location in handle go: {new_game.current_location}")
            # play a sound on channel 0 with a max time of 2000 milliseconds
            #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=2000)
            new_game.counter += 1
            new_game.location_data.show_location_data()
        else:
            print(f"Invalid choice. You cannot go {noun} Try again")
        
    def handle_start(self, noun):
        print(f"Handling START command for {noun}")

    def handle_enter(self, noun):
        print(f"Handling ENTER command for {noun}")

    def handle_go_mazda(self, noun):
        global car_started
        if car_started == False:
            messagebox.showinfo("showinfo", 'Please start your car to continue on')
            print('Please start your car to continue on')
        else:
            self.handle_go_norm(noun)

    def handle_get(self, noun):
        print(f"Handling GET command for {noun}")

    def handle_drop(self, noun):
        print(f"Handling DROP command for {noun}")

    def handle_look(self, noun):
        print(f"Handling LOOK command for {noun}")

    def handle_talk(self, noun):
        print(f"Handling TALK command for {noun}")

class GameCommand:   
    def __init__(self):
        self.previous_commands = []
        self.previous_locations = []

    def show_history(self):
        pass

    def handle_input(self, command):
        if command in ['save']:
            print(f"Handling SAVE command for {command}")
        elif command in ['load']:
            pass
        elif command in ['musicon']:
            pass
        elif command in ['musicoff']:
            pass
        elif command in ['musicup']:
            pass
        elif command in ['musicdown']:
            pass
        elif command in ['sfxon']:
            pass
        elif command in ['sfxoff']:
            pass
        elif command in ['sfxup']:
            pass
        elif command in ['sfxdown']:
            pass
        elif command in ['help']:
            pass
        elif command in ['inventory']:
            pass
        elif command in ['map']:
            pass
        elif command in ['history']:
            pass
        elif command in ['quit']:
            pass
        else:
            new_game.text_parser.parse_command(command)

class GameEngine:
    def __init__(self):
        self.player = Player()
        self.location_data = LocationData()
        self.counter = 0
        self.insideMazda = False
        self.car_started = False
        self.current_location = 'Elevator'
        self.commander = GameCommand()
        self.text_parser = TextParser()

    def play_game(self):
        self.current_location = 'Elevator'
        self.location_data.show_location_data()
        while True:
            user_input = input("What would you like to do next? (type 'help' to see valid commands or 'quit' to exit): \n>> ").strip().lower()
            self.commander.handle_input(user_input)

new_game = GameEngine()

if __name__ == "__main__":   
    pass
    #start_game()
    new_game.play_game()