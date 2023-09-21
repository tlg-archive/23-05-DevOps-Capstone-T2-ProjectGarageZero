import tkinter as tk
import os
import json
import random
from tkinter import Frame, messagebox
from functionsTest import directions_data, locations_data, items_data, descriptions_data
from interaction import data as npc_data

#helper functions
script_dir = os.path.dirname(os.path.realpath(__file__))
text_file = os.path.join(script_dir, 'data', 'game-text.json')

def convert_json():
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text
game_text = convert_json()

#initilize the tkinter window and size
gui_window = tk.Tk()
gui_window.geometry("500x500")
#print(gui_window.winfo_width(), type(gui_window.winfo_width()))

#HELP TEXT
def display_help():
    messagebox.showinfo("showinfo", game_text["help"])

def display_quit():
    answer = messagebox.askyesno("askyesno", game_text["quit"])
    if answer:
        gui_window.destroy()

#MENUBAR
menubar = tk.Menu(gui_window)
gui_window.config(menu=menubar)

#MENU ITEMS
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Help", command=display_help)

quit_menu = tk.Menu(menubar, tearoff=0)
quit_menu.add_command(label="Quit", command=display_quit)

menubar.add_cascade(menu=help_menu, label="Help")
menubar.add_cascade(menu=quit_menu, label="Quit Game")

def show_frame(frame):
    frame.tkraise()

#all main frames
title_frame = Frame(gui_window,width=500, height=500)
#title_frame.pack()

game_frame = Frame(gui_window,width=500, height=500)
dialogue_frame = Frame(gui_window,width=500, height=500)

title_frame.place(in_=gui_window, x=0, y=0, relwidth=1, relheight=1)
game_frame.place(in_=gui_window, x=0, y=0, relwidth=1, relheight=1)
dialogue_frame.place(in_=gui_window, x=0, y=0, relwidth=1, relheight=1)
show_frame(title_frame)


#general label settings
title_label = tk.Label(title_frame, text=game_text["title"], wraplength=500)
title_label.pack()

def choose_start(event=None):
    command = command_line.get()
    if command in ['1', 'start', 'start game']:
        #start_game()
        print('Start Game')
        #title_frame.destroy()
        start_game()
    elif command in ['2', 'quit', 'exit']:
        #clear_screen()
        display_quit()
        print("Goodbye!\n")
        #display_quit()
    else:
        messagebox.showinfo("showinfo", f"Invalid Choice. Please follow instructions on screen.")
        print("Invalid choice. Press Enter to continue...")

#example text input
command_line = tk.Entry(title_frame)
command_line.bind('<Return>', choose_start)
command_line.pack()

#example button
start_button = tk.Button(title_frame, text="Start Game", command = choose_start)
start_button.pack()
# Get and print the current location's description

#Game Frame Stuff
def start_game():
    #game_frame = Frame(gui_window)
    #game_frame.pack()
    #game_frame.tkraise()
    show_frame(game_frame)
    #game_frame.pack()
    update_game_text()
    # Set initial location

# Set initial location
current_location = 'Elevator'
counter = 0
inventory = []
car_started = False

game_frame.columnconfigure(0, weight=1)
game_frame.columnconfigure(1, weight=2)

location_status = tk.Label(game_frame)
#location_status.pack()
location_status.grid(row=0, column=0)

output_text = tk.Label(game_frame)
#output_text.pack()
output_text.grid(row=1, column=0)

desc_frame = Frame(game_frame)
desc_frame.grid(row=2, column=0)
tk.Label(desc_frame, text='I WORK').pack()
#item_desc = tk.Label(game_frame)
#item_desc.grid(row=2, column=0)
#output_text.pack()

items_frame = Frame(game_frame)
#items_frame.pack()
items_frame.grid(row=3, column=0)

choices_frame = Frame(game_frame)
#choices_frame.pack()
choices_frame.grid(row=4, column=0)

inventory_frame = Frame(game_frame)
inventory_frame.grid(row=0, column=1)

def get_location_data():
    print(f"CURRENT LOCATION IN GET LOCATION DATA: {current_location}")
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

def get_npc(npc_name):
    for npc in npc_data['NPCs']:
        if npc['Name'] == npc_name:
            #print(f"FOUND EM: {npc}")
            return npc
    return None

def greet_npc(npc):
    if 'Greetings' in npc:
        return random.choice(npc['Greetings'])

def proccess_npc_input():
    user_input = game_command.get().strip()
    game_command.delete(0, tk.END)
    text_parser.parse_command(user_input)

def talk_npc(choice,npc):
    print(f"choice: {choice}")
    print(f"Chatting: {npc}")
    #for widget in dialogue_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        #widget.destroy()
    

def interact_with_npc(npc):
    print('I WORK')
    show_frame(dialogue_frame)
    print('I WORK')
    #dialogue_frame.pack()
    tk.Label(dialogue_frame, text=f"Talking with: {npc['Name']}")
    tk.Label(dialogue_frame,text=greet_npc(npc)).pack()
    """ npc_title.configure()
    npc_response.configure() """
    npc_command = tk.Entry(dialogue_frame)
    npc_command.bind('<Return>', proccess_npc_input)

    for choice in npc['PlayerChoices']:
        player_choice = choice['Choice']
        tk.Button(dialogue_frame, text=choice['Choice'], command = lambda: talk_npc(player_choice, npc)).pack()
        #print(f"{idx + 1}. {choice['Choice']}", command = talk_npc)

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

    #item_desc.configure(text=" ", bg='#ECECEC', fg='#f00', pady=0, padx=0, font=10)

# Function to update the game text
def update_game_text():
    #output_text.delete(1.0, tk.END)
    #print("LOCATIONS DATA",current_location_data)
    print(f'Desc frame loaded: {desc_frame.winfo_children()}')
    global inventory
    current_location_data, available_directions, available_items = get_location_data()
    # Print the current location
    location_head = f"LOCATION: {current_location}"
    move_head = f"MOVES MADE: {counter}"
    #print(f"current inventory: {inventory}")

    # Printing header
    location_status.configure(text=f"{location_head}\n{move_head}")
    output_text.configure(text=current_location_data["Description"],wraplength=500)
    if available_items:
        tk.Label(items_frame, text='ITEMS').pack()
        for item in available_items:
            tk.Label(items_frame, text=item).pack()

    tk.Label(choices_frame, text='EXITS').pack()
    for direction_data in available_directions:
        tk.Label(choices_frame,text=f"{direction_data['Direction']} - {direction_data['Destination']}").pack()

    #Update inventory frame
    tk.Label(inventory_frame, text="INVENTORY").pack()
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
        print(f"verb {verb} noun {noun}")

        if verb == 'save':
            self.save_game()
            print(game_text["save_game"])
            return

        if verb == 'load':
            self.load_game()
            print(game_text["load_game"])
            return

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
        print(f'inventory: {inventory}')
        if 'mazda' in inventory:
            self.handle_go_mazda(noun)
        else:
            self.handle_go_norm(noun)
    
    def handle_go_norm(self, noun):
        print(f"Handling GO command for {noun}")
        global current_location  # Declare current_location as global
        global current_location_data
        global counter
        current_location_data = get_location_data()[0]
        #print(f"noun in GO: {noun}")
        #print(f"current location: {current_location}")
        #print(f"current location data: {current_location_data['Directions']}")
        if noun.title() in current_location_data["Directions"]:
            choice = noun.title()
            current_location = current_location_data["Directions"][choice]
            #print(f'CURRENT LOCATION: {current_location}')
            #test_location()
            counter += 1
            clear_choices()
            update_game_text()
            #text_parser.parse_command(noun)
        else:
            messagebox.showinfo("showinfo", f"Invalid choice. You cannot go {noun} Try again")
            print("Invalid choice. Try again")
        
    def handle_start(self, noun):
        #set car start == true
        global car_started
        if 'mazda' in inventory:
            if car_started == False:
                car_started = True
                print('You started car your car')
            else:
                messagebox.showinfo("showinfo", 'Your car is already started')
                print('Your car is already started')
        else:
            messagebox.showinfo("showinfo", "You can't start anything right now. Have you found your car yet?")
            print("You can't start anything right now. Have you found your car yet?")

    def handle_enter(self, noun):
        if current_location == 'Parking West 2' and 'mazda' not in inventory:
            # Add the "mazda" to the inventory
            inventory.append('mazda')
            # play a sound on channel 0 with a max time of 1500 milliseconds
            #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/cardoor.mp3'), maxtime=1500)
            clear_choices()
            tk.Label(desc_frame,text=f"You have entered the Mazda.",bg='#fff', fg='#f00', pady=10, padx=10, font=15).pack()
            update_game_text()
            print("You have entered the Mazda.")
        elif 'mazda' in inventory:
            print("You are already in the Mazda.")
            messagebox.showinfo("showinfo", "You are already in the Mazda.")
        else:
            messagebox.showinfo("showinfo", f'You cannot enter {noun}')
            print(f'You cannot enter {noun}')

    def handle_go_mazda(self, noun):
        print('I HAVE A CAR!!!!!')
        global car_started
        if car_started == False:
            messagebox.showinfo("showinfo", 'Please start your car to continue on')
            print('Please start your car to continue on')
        else:
            print('vroom vroom')
            self.handle_go_norm(noun)

    def handle_get(self, noun):
        print(f"Handling GET command for {noun}")
        # Check if the item is in the current room
        global available_items
        global current_location
        global inventory
        available_items = get_location_data()[2]
        if noun in available_items:
            # Call the get_item function to pick up the item
            # play a sound on channel 0 with a max time of 1250 milliseconds
            #pygame.mixer.Channel(0).play(pygame.mixer.Sound('./sound/get.mp3'), maxtime=1250)
            # Check if the item is in the current location
            for item_data in items_data['Items']:
                if item_data['Name'].lower() == noun and item_data['Location'] == current_location:
                    inventory.append(item_data['Name'])
                    # Remove the item from the current location
                    items_data['Items'].remove(item_data)
                    print(f"You now have {item_data['Name']}.")
                    #print(item_desc.c)
                    #item_desc.configure(text=f"You now have {item_data['Name']}.", bg='#fff', fg='#f00', pady=10, padx=10, font=15)
                    #tk.Label(desc_frame,text=f"You now have {item_data['Name']}.").pack()
                    obtained_item = item_data['Name']
                    #return
            clear_choices()
            tk.Label(desc_frame,text=f"You now have {obtained_item}.",bg='#fff', fg='#f00', pady=10, padx=10, font=15).pack()
            update_game_text()
        else:
            messagebox.showinfo("showinfo", "That's not here! (hint: type the name exactly)")
            print(f"{noun} is not here! (hint: type the name exactly)")

    def handle_drop(self, noun):
        print(f"Handling DROP command for {noun}")
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
            print(f"You dropped {noun}.")
            clear_choices()
            update_game_text()
        else:
            messagebox.showinfo("showinfo", f"You don't have {noun} on you!")
            print("You don't have that on you!")

    def handle_look(self, noun):
        print(f"Handling LOOK command for {noun}")
        global available_items
        available_items = get_location_data()[2]
        if noun in available_items:
            for item_data in items_data['Items']:
                if item_data['Name'].lower() == noun:
                    print(item_data['Description'])
                    #item_desc.configure(text=item_data['Description'], bg='#fff', fg='#f00', pady=10, padx=10, font=15)
                    look_item = item_data['Description']
                    #return
            clear_choices()
            tk.Label(desc_frame,text=f"You now have {look_item}.",bg='#fff', fg='#f00', pady=10, padx=10, font=15).pack()
            update_game_text()
        else:
            #print("That item is not here or cannot be examined.")
            messagebox.showinfo("showinfo", f"The item '{noun}' is not here or cannot be examined.")

    def handle_talk(self, noun):
        print(f"Handling TALK command for {noun}")
        npc = get_npc(noun)  
        if npc:
            print(f"found npc: {noun}")
            interact_with_npc(npc)  
        else:
            messagebox.showinfo("showinfo", f"No NPC named {noun} found.")
            print(f"No NPC named {noun} found.")

# Function to handle user input
text_parser = TextParser()
def process_input(event=None):
    user_input = game_command.get().strip()
    game_command.delete(0, tk.END)
    text_parser.parse_command(user_input)

game_command = tk.Entry(game_frame)
game_command.bind('<Return>', process_input)
#game_command.pack()
game_command.grid(row=5, column=0)

if __name__ == "__main__":
    gui_window.mainloop()