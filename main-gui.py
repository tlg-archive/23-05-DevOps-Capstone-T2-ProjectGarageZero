import tkinter as tk
import os
import json
import random
from functools import partial
from tkinter import Frame, messagebox, Toplevel, LabelFrame
from functionsTest import directions_data, locations_data, items_data
from interaction import data as npc_data
import pickle
import pygame
#Suppressing Pygame support prompt that was displaying pre-splash screen
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

#helper functions
script_dir = os.path.dirname(os.path.realpath(__file__))
text_file = os.path.join(script_dir, 'data', 'game-text.json')
map_file = os.path.join(script_dir, 'data', 'map-file.txt')
bg_music = os.path.join(script_dir, 'sound', 'garage_music.ogg')

help_sfx = os.path.join(script_dir, 'sound', 'help.mp3')
go_sfx = os.path.join(script_dir, 'sound', 'go.mp3')
get_sfx = os.path.join(script_dir, 'sound', 'get.mp3')
map_sfx = os.path.join(script_dir, 'sound', 'map.mp3')
cardoor_sfx = os.path.join(script_dir, 'sound', 'cardoor.mp3')
carstart_sfx = os.path.join(script_dir, 'sound', 'carstart.mp3')
drop_sfx = os.path.join(script_dir, 'sound', 'drop.mp3')

def convert_json():
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text
game_text = convert_json()

def gen_map():
    with open(map_file, "r") as file:
        map_list = file.readlines()
    return map_list

#initilize the tkinter window and size
gui_window = tk.Tk()
gui_window.title("Project Garage Zero")
gui_window.minsize(700,400)

def show_frame(frame):
    frame.tkraise()

#all main frames
title_frame = Frame(gui_window,width=500, height=500)
game_frame = Frame(gui_window,width=500, height=500)
dialogue_frame = Frame(gui_window,width=500, height=500)

title_frame.place(in_=gui_window, x=0, y=0, relwidth=1, relheight=1)
game_frame.place(in_=gui_window, x=0, y=0, relwidth=1, relheight=1)
dialogue_frame.place(in_=gui_window, x=0, y=0, relwidth=1, relheight=1)

show_frame(title_frame)


#MUSIC FUNCTIONALITY
# Setting current music volume value

class SoundController:
    def __init__(self):
        # Setting current music volume value
        self.current_music_volume=.3
        # Setting current SFX volume value
        self.current_sfx_volume = 0.5

    def background_music(self):
        song_name_list = bg_music.split('/')
        array_len = len(song_name_list)
        sound_file_path = os.path.join(script_dir, 'sound', song_name_list[array_len-1])

        pygame.init()
        pygame.mixer.init()
        s = 'sound'  # folder for music and FX
        music = pygame.mixer.Sound(sound_file_path)
        pygame.mixer.music.load(sound_file_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.current_music_volume)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def volume_up(self):
        #global current_music_volume
        self.current_music_volume += 0.1 
        pygame.mixer.music.set_volume(self.current_music_volume)
    
    def volume_down(self):
        #global current_music_volume
        self.current_music_volume -= 0.1
        pygame.mixer.music.set_volume(self.current_music_volume)

    def setup_sfx(self):
        pygame.mixer.set_num_channels(8) 

    def sfx_on(self):
        pygame.mixer.Channel(0).set_volume(self.current_sfx_volume)

    def sfx_off(self):
        pygame.mixer.Channel(0).set_volume(0.0)

    def sfx_volume_up(self):
        #global current_sfx_volume
        self.current_sfx_volume += 0.1
        pygame.mixer.Channel(0).set_volume(self.current_sfx_volume)

    def sfx_volume_down(self):
        #global current_sfx_volume
        self.current_sfx_volume -= 0.1
        pygame.mixer.Channel(0).set_volume(self.current_sfx_volume)

    def play_sfx(self,sound_file):
        song_name_list = sound_file.split('/')
        array_len = len(song_name_list)
        sound_file_path = os.path.join(script_dir, 'sound', song_name_list[array_len-1])
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_file_path), maxtime=2000)

game_sound = SoundController()
#HELP TEXT
def display_help():
    game_sound.play_sfx(help_sfx)
    #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/help.mp3'), maxtime=2000)
    messagebox.showinfo("showinfo", game_text['help'])

def display_quit():
    answer = messagebox.askyesno("askyesno", game_text["quit"])
    if answer:
        gui_window.destroy()

def show_map(map_list):
    map_array = []
    for line in map_list:
        map_array.append(line)
    return map_array

def display_map():
    map_list = gen_map()
    game_map_array = show_map(map_list)
    game_map = ''.join(game_map_array)
    #print(game_map)
    game_sound.play_sfx(map_sfx)
    #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/map.mp3'), maxtime=1000)
    messagebox.showinfo("showinfo", game_map)

def display_sound():
    newWindow = Toplevel(gui_window)
    #newWindow.minsize(400,400)
    newWindow.title("Sound Settings")
    #newWindow.grid(row=0, column=0)
    #Label(newWindow, text="Sound Settings").pack()

    volume_frame = LabelFrame(newWindow, text="Volume")
    volume_frame.grid(row=0, column=0, pady=10, padx=10)

    sfx_frame = LabelFrame(newWindow, text="Sound Effect")
    sfx_frame.grid(row=1, column=0, pady=10, padx=10)
    
    #Checkboxes for sound on or off

    bgm_state = tk.IntVar(value=1)
    sfx_state = tk.IntVar(value=1)

    def volume_toggle():
        if bgm_state.get() == 1:
            pygame.mixer.music.set_volume(game_sound.current_music_volume)
        else:
            pygame.mixer.music.set_volume(0.0)

    def sfx_toggle():
        if sfx_state.get() == 1:
            game_sound.sfx_on()
            game_sound.play_sfx(get_sfx)
        else:
            game_sound.sfx_off()

    bgm_check = tk.Checkbutton(volume_frame, text="Background Music ON or OFF", variable=bgm_state, command=volume_toggle)
    bgm_check.grid()

    sfx_check = tk.Checkbutton(sfx_frame, text="Background Music ON or OFF", variable=sfx_state, command=sfx_toggle)
    sfx_check.grid()

    #SLIDERS FOR SOUND LEVELS
    def volume_slide(vol):
        #vol = vol/100
        game_sound.current_music_volume = volume_slider.get()/100
        pygame.mixer.music.set_volume(game_sound.current_music_volume)

    def sfx_slide(vol):
        game_sound.current_sfx_volume = sfx_slider.get()/100
        pygame.mixer.Channel(0).set_volume(game_sound.current_sfx_volume)
        game_sound.play_sfx(get_sfx)

    volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient="vertical", command = volume_slide)

    volume_slider.set(game_sound.current_music_volume*100)
    volume_slider.grid()

    sfx_slider = tk.Scale(sfx_frame, from_=0, to=100, orient="vertical", command = sfx_slide)
    sfx_slider.set(game_sound.current_sfx_volume*100)
    sfx_slider.grid()

# Save game functionality
previous_commands = []
previous_locations = []
def save_game():
    game_state = {
        "current_location": current_location,
        "counter": counter,
        "inventory": inventory,
        "items_data": items_data,
        "previous_commands": previous_commands,
        "previous_locations": previous_locations,
        "current_music_volume": game_sound.current_music_volume,
        "current_sfx_volume": game_sound.current_sfx_volume,
        "car_started": car_started
    }
    
    with open('saved_game_gui.pkl', 'wb') as file:
        pickle.dump(game_state, file)

    messagebox.showinfo("showinfo", "Your game has been saved!")
    print("Game saved!")

def load_game():
    global current_location, counter, inventory, items_data, previous_commands, previous_locations, car_started
    try:
        with open('saved_game_gui.pkl', 'rb') as file:
            game_state = pickle.load(file)

        current_location = game_state['current_location']
        counter = game_state['counter']
        inventory = game_state['inventory']
        items_data = game_state['items_data']
        previous_commands = game_state['previous_commands']
        previous_locations = game_state['previous_locations']
        game_sound.current_music_volume = game_state['current_music_volume']
        game_sound.current_sfx_volume = game_state['current_sfx_volume']
        car_started = game_state["car_started"]

        print("Game successfully loaded!")
        messagebox.showinfo("showinfo", "Game successfully loaded!")
        clear_choices()
        start_game()
    except FileNotFoundError:
        print("No saved game found!")
        messagebox.showinfo("showinfo", "No saved game found!")

def display_history():
    #print("History:")
    command_history = ["COMMAND HISTORY"]
    for i in range(min(len(previous_locations), len(previous_commands))):
        line = f"You used the '{previous_commands[i]}' command in the '{previous_locations[i]}'"
        #print(line)
        command_history.append(line)

    if len(command_history) == 0:
        messagebox.showinfo("showinfo", "You don't have any saved commands. Play the game to get some!")
    else:
        messagebox.showinfo('Command History', '\n\n'.join(''.join(command) for command in command_history))

#MENUBAR SECTION
menubar = tk.Menu(gui_window)
gui_window.config(menu=menubar)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Help", command=display_help)

game_options_menu = tk.Menu(menubar, tearoff=0)
game_options_menu.add_command(label="Show Map", command=display_map)
game_options_menu.add_command(label="Show Input History", command=display_history)
game_options_menu.add_command(label="Save Game", command=save_game)
game_options_menu.add_command(label="Load Game", command=load_game)

sound_menu = tk.Menu(menubar, tearoff=0)
sound_menu.add_command(label="Sound Settings", command=display_sound)

quit_menu = tk.Menu(menubar, tearoff=0)
quit_menu.add_command(label="Return to Title Screen", command=lambda: show_frame(title_frame))
quit_menu.add_command(label="Quit", command=display_quit)

menubar.add_cascade(menu=game_options_menu, label="Game Options")
menubar.add_cascade(menu=sound_menu, label="Sound Options")
menubar.add_cascade(menu=quit_menu, label="Quit Game")
menubar.add_cascade(menu=help_menu, label="Help")

def start_game():
    show_frame(game_frame)
    update_game_text()

#Title Frame Items
title_label = tk.Label(title_frame, text=game_text["title"], wraplength=500)
title_label.pack()

start_button = tk.Button(title_frame, text="Start Game", command = start_game)
start_button.pack()

load_button = tk.Button(title_frame, text="Load Game", command = load_game)
load_button.pack()

quit_button = tk.Button(title_frame, text="Quit Game", command = display_quit)
quit_button.pack()

#Game Frame Stuff
current_location = 'Elevator'
counter = 15
inventory = []
car_started = False

#game_frame.rowconfigure(0, weight=1)
game_frame.columnconfigure(0, weight=1)
game_frame.columnconfigure(1, weight=2)

location_status = tk.Label(game_frame)
location_status.grid(row=0, column=0)

output_text = tk.Label(game_frame)
output_text.grid(row=1, column=0)

desc_frame = Frame(game_frame)
desc_frame.grid(row=2, column=0)

items_frame = Frame(game_frame)
items_frame.grid(row=3, column=0)

choices_frame = Frame(game_frame)
choices_frame.grid(row=4, column=0)

inventory_frame = Frame(game_frame)
inventory_frame.grid(row=0, column=1)

#Items within the dialogue frame
dialogue_frame.columnconfigure(0, weight=1)
npc_title = tk.Label(dialogue_frame)
npc_title.grid(row=0, column=0)

npc_response = tk.Label(dialogue_frame)
npc_response.grid(row=1, column=0)

answer_frame = Frame(dialogue_frame)
answer_frame.grid(row=2, column=0)

def get_location_data():
    #print(f"CURRENT LOCATION IN GET LOCATION DATA: {current_location}")
    #print(f"LOCATION LOOP: {locations_data['Locations']}")
    for location in locations_data['Locations']:
        #print(f"LOCATION LOOP: {location}")
        if location['Name'] == current_location:
            new_location_data = location
            #print(f"NEW LOCATION DATA: {new_location_data}")
            break

    current_directions = []
    for location_data in directions_data['Directions']:
        if location_data['Location'] == current_location:
            current_directions = location_data['Directions']
            break

    # Get items in room
    available_items = []
    for item_data in items_data['Items']:
        if item_data['Location'] == current_location:
            available_items.append(item_data['Name'])

    #print(f"ITEMS: {available_items}")
    return [new_location_data, current_directions, available_items]

#NPC INTERACTION SECTION
def get_npc(npc_name):
    for npc in npc_data['NPCs']:
        if npc['Name'] == npc_name:
            #print(f"FOUND EM: {npc}")
            return npc
    return None

def greet_npc(npc):
    if 'Greetings' in npc:
        return random.choice(npc['Greetings'])

def beat_game():
    messagebox.showinfo("showinfo", "Congratulations! You successfully exited the parking lot with your car! \nThanks for playing!!!!!!")
    gui_window.destroy()

def talk_npc(choice,npc_ans, npc_data):
    #print(f"choice: {choice}")
    #print(f"Chatting: {npc_ans}")
    #print(f"NPC DATA {npc_data}")
    global current_location
    global inventory
    #npc_response.configure(text=npc_ans)
    if npc_data['Name'].lower() == "attendant":
        if choice == "yes":
            if 'mazda' in inventory:
                npc_response.configure(text=npc_ans)
                #print("Congratulations! You successfully exited the parking lot with your car!")
                beat_game()
            else:
                npc_response.configure(text="Where's your car?")
        elif choice == "Offer lollipop":
            if "Lollipop" in inventory:
                npc_response.configure(text=npc_ans)
                beat_game()
                #print("Congratulations! You successfully exited the parking lot with your car!")
            else:
                npc_response.configure(text="-____- You don't have a lollipop...")
        else:
            npc_response.configure(text=npc_ans)
    elif npc_data['Name'].lower() == "creepy man":
        if choice == 'Offer pack of gum' and 'gum' in inventory:
            inventory.remove('gum')
            inventory.append('Lollipop')
            #new_game.player.add_to_inventory(selected_choice["Reward"])
            print(f"You received a Lollipop!")
            npc_response.configure(text=npc_ans)
        elif choice == 'Offer pack of gum' and 'gum' not in inventory:
            npc_response.configure(text="You don't even have any gum....")
        else:
            npc_response.configure(text=npc_ans)

def return_to_game(npc_name):
    #print('RETURN TO THE MAIN GAME')
    answer = messagebox.askyesno("askyesno", f"Do you want to leave the conversation with {npc_name}?")
    if answer:
        clear_choices()
        update_game_text()
        show_frame(game_frame)

def interact_with_npc(npc):
    #clear_choices()
    show_frame(dialogue_frame)

    npc_title.configure(text=f"Talking with: {npc['Name']}")
    npc_response.configure(text=greet_npc(npc))
    
    for index, btn_name in enumerate(npc['PlayerChoices']):
        btn = tk.Button(answer_frame, text=str(btn_name['Choice']), command=partial(talk_npc, btn_name['Choice'], btn_name['Response'], npc))
        btn.grid(row=index+2, column=0)

    exit_npc = tk.Button(answer_frame, text="Leave Conversation", command= lambda: return_to_game(npc['Name']))
    exit_npc.grid(row=len(npc['PlayerChoices'])+2, column=0)
    
def clear_choices():
    #print(' I AM IN THE FUNCGIOJTR')
    #print(f"children in choices frame: {choices_frame.winfo_children()}")
    for widget in choices_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        widget.destroy()

    for widget in items_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        widget.destroy()
    for widget in inventory_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        widget.destroy()
    for widget in desc_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        widget.destroy()
    """ for widget in dialogue_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        widget.destroy() """

# Function to update the game text
def update_game_text():
    #output_text.delete(1.0, tk.END)
    #print("LOCATIONS DATA",current_location_data)
    #print(f'Desc frame loaded: {desc_frame.winfo_children()}')
    global inventory
    current_location_data, available_directions, available_items = get_location_data()
    # Print the current location
    location_head = f"LOCATION: {current_location}\n"
    move_head = f"MOVES MADE: {counter}\n"
    #print(f"current inventory: {inventory}")

    # Printing header
    location_status.configure(text=f"{location_head}\n{move_head}", font='Helvetica 16 bold')
    output_text.configure(text=current_location_data["Description"],wraplength=500)
    if available_items:
        tk.Label(items_frame, text='ITEMS',font='Helvetica 16 bold').pack()
        for item in available_items:
            tk.Label(items_frame, text=item).pack()

    tk.Label(choices_frame, text='EXITS',font='Helvetica 14 bold').pack()
    for direction_data in available_directions:
        tk.Label(choices_frame,text=f"{direction_data['Direction']} - {direction_data['Destination']}").pack()

    #Update inventory frame
    tk.Label(inventory_frame, text="INVENTORY",font='Helvetica 14 bold').pack()
    for item in inventory:
        tk.Label(inventory_frame, text=item).pack()
    
    #output_text.insert(tk.END, current_location_data["Description"])

def test_location():
    print(f"NEW CURRENT LOCATION:{current_location}")
    current_location_data = get_location_data()[0]
    available_directions = get_location_data()[1]
    print("LOCATIONS DATA",current_location_data)
    print("DIRECTIONS DATA",available_directions)

class TextParser():
    def __init__(self):
        self.locations = {}

    def parse_command(self, command):
        #global inventory
        command_words = command.split(' ')
        print(command_words)
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
        #print(f'inventory: {inventory}')
        if 'mazda' in inventory:
            self.handle_go_mazda(noun)
        else:
            self.handle_go_norm(noun)
    
    def handle_go_norm(self, noun):
        #print(f"Handling GO command for {noun}")
        global current_location  # Declare current_location as global
        global current_location_data
        global counter
        current_location_data = get_location_data()[0]
        #print(f"noun in GO: {noun}")
        #print(f"current location: {current_location}")
        #print(f"current location data: {current_location_data['Directions']}")
        if counter == 1:
            messagebox.showinfo("showinfo", "OH NO! Time is up and you did not leave the parking lot before you had to pay the extra parking fee. Try again and see if you can get your car and leave!")
            gui_window.destroy()

        if noun.title() in current_location_data["Directions"]:
            choice = noun.title()
            current_location = current_location_data["Directions"][choice]
            #print(f'CURRENT LOCATION: {current_location}')
            #test_location()
            if 'mazda' in inventory and current_location == 'Elevator':
                messagebox.showinfo("showinfo", "You can't bring your car on the elevator.")
                return
            counter -= 1
            clear_choices()
            update_game_text()
            game_sound.play_sfx(go_sfx)
            #text_parser.parse_command(noun)
        else:
            messagebox.showinfo("showinfo", f"Invalid choice. You cannot go {noun} Try again")
            print("Invalid choice. Try again")
        
    def handle_start(self, noun):
        #set car start == true
        global car_started
        if noun == 'mazda':
            if 'mazda' in inventory:
                if car_started == False:
                    car_started = True
                    #print('You started car your car')
                    #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/carstart.mp3'), maxtime=5000)
                    game_sound.play_sfx(carstart_sfx)
                    messagebox.showinfo("showinfo", "You started car your car. You can drive around the parking lot now.")
                else:
                    messagebox.showinfo("showinfo", 'Your car is already started')
                    #print('Your car is already started')
        else:
            messagebox.showinfo("showinfo", "You can't start anything right now. Have you found your car yet?")
            #print("You can't start anything right now. Have you found your car yet?")

    def handle_enter(self, noun):
        global current_location
        if noun == 'mazda':
            if current_location == 'Parking West 2' and 'mazda' not in inventory:
                # Add the "mazda" to the inventory
                self.handle_get(noun)
            elif 'mazda' in inventory:
                #print("You are already in the Mazda.")
                messagebox.showinfo("showinfo", "You are already in the Mazda.")
        else:
            messagebox.showinfo("showinfo", f'You cannot enter {noun}')
            #print(f'You cannot enter {noun}')

    def handle_go_mazda(self, noun):
        global car_started
        if car_started == False:
            messagebox.showinfo("showinfo", 'Please start your car to continue on')
            #print('Please start your car to continue on')
        else:
            self.handle_go_norm(noun)

    def handle_get(self, noun):
        #print(f"Handling GET command for {noun}")
        # Check if the item is in the current room
        global available_items
        global current_location
        global inventory
        available_items = get_location_data()[2]
        if noun in available_items:
            # Call the get_item function to pick up the item
            # play a sound on channel 0 with a max time of 1250 milliseconds
            # Check if the item is in the current location
            for item_data in items_data['Items']:
                if item_data['Name'].lower() == noun and item_data['Location'] == current_location:
                    inventory.append(item_data['Name'])
                    # Remove the item from the current location
                    items_data['Items'].remove(item_data)
                    #print(f"You now have {item_data['Name']}.")
                    obtained_item = item_data['Name']
                    #return
            clear_choices()
            tk.Label(desc_frame,text=f"You now have {obtained_item}.",bg='#fff', fg='#f00', pady=10, padx=10, font=15).pack()
            if noun == 'mazda':
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
                game_sound.play_sfx(cardoor_sfx)
            else:
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/get.mp3'), maxtime=1000)
                game_sound.play_sfx(get_sfx)
            update_game_text()
        else:
            messagebox.showinfo("showinfo", f"{noun} not here! (hint: type the name exactly)")
            #print(f"{noun} is not here! (hint: type the name exactly)")

    def handle_exit(self, noun):
        if noun == 'mazda':
            if 'mazda' in inventory:
                # Remove the Mazda from the inventory
                self.handle_drop('mazda')
            else:
                messagebox.showinfo("showinfo", f"You are not inside the Mazda.")
                #print("You are not inside the Mazda.")
        else:
            messagebox.showinfo("showinfo", f"You can't exit {noun}")

    def handle_drop(self, noun):
        #print(f"Handling DROP command for {noun}")
        if noun in inventory:
            # Dictionary for item data
            item_to_drop = {
                "Name": noun,
                "Location": current_location,
                "Use": "none",
                "Type": "none",
                "Note": "none",
                "Description": f"A {noun} on the ground."
            }

            # Add the item to the current location's items
            items_data['Items'].append(item_to_drop)
            # Remove the item from the player's inventory
            inventory.remove(noun)
            #print(f"You dropped {noun}.")
            clear_choices()
            if noun == 'mazda':
                tk.Label(desc_frame,text=f"You have exited the Mazda.",bg='#fff', fg='#f00', pady=10, padx=10, font=15).pack()
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
                game_sound.play_sfx(cardoor_sfx)
            else:
                tk.Label(desc_frame,text=f"You dropped {noun}.",bg='#fff', fg='#f00', pady=10, padx=10, font=15).pack()
                #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/go.mp3'), maxtime=1000)
                game_sound.play_sfx(drop_sfx)
            update_game_text()
        else:
            messagebox.showinfo("showinfo", f"You don't have {noun} on you!")
            #print("You don't have that on you!")

    def handle_look(self, noun):
        #print(f"Handling LOOK command for {noun}")
        global available_items
        available_items = get_location_data()[2]
        if noun in available_items:
            for item_data in items_data['Items']:
                if item_data['Name'].lower() == noun:
                    print(item_data['Description'])
                    look_item = item_data['Description']
                    
            clear_choices()
            tk.Label(desc_frame,text=f"You now have {look_item}.",bg='#fff', fg='#f00', pady=10, padx=10, font=15,wraplength=500).pack()
            update_game_text()
        else:
            #print("That item is not here or cannot be examined.")
            messagebox.showinfo("showinfo", f"The item '{noun}' is not here or cannot be examined.")

    def handle_talk(self, noun):
        #print(f"Handling TALK command for {noun}")
        npc = get_npc(noun)  
        if npc:
            #print(f"found npc: {noun}")
            interact_with_npc(npc)  
        else:
            messagebox.showinfo("showinfo", f"No NPC named {noun} found.")
            #print(f"No NPC named {noun} found.")

# Function to handle user input
text_parser = TextParser()
def process_input(event=None):
    global previous_commands
    global previous_locations
    global current_location
    
    user_input = game_command.get().strip()
    game_command.delete(0, tk.END)
    text_parser.parse_command(user_input)
    previous_commands.append(user_input)
    previous_locations.append(current_location)

game_command = tk.Entry(game_frame)
game_command.bind('<Return>', process_input)
game_command.grid(row=5, column=0)

if __name__ == "__main__":
    game_sound.background_music()
    game_sound.setup_sfx()
    gui_window.mainloop()