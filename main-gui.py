import tkinter as tk
import os
import json
from tkinter import Frame, BooleanVar, messagebox
from functionsTest import directions_data, locations_data, items_data, descriptions_data

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
#gui_window.geometry("500x500")

#HELP TEXT
def display_help():
    print("YEY")
    messagebox.showinfo("showinfo", game_text["help"])


#MENUBAR
menubar = tk.Menu(gui_window)
gui_window.config(menu=menubar)

#HELP
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Help", command=display_help)

menubar.add_cascade(menu=help_menu, label="Help")

#title frame
title_frame = Frame(gui_window)
title_frame.pack()

#all frames
game_frame = Frame(gui_window)

#general label settings
title_label = tk.Label(title_frame, text=game_text["title"])
title_label.pack()

def choose_start(event=None):
    command = command_line.get()
    if command in ['1', 'start', 'start game']:
        #start_game()
        print('Start Game')
        title_frame.destroy()
        start_game()
    elif command in ['2', 'quit', 'exit']:
        #clear_screen()
        print("Goodbye!\n")
        #sys.exit()
    else:
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
    game_frame.tkraise()
    game_frame.pack()
    # Set initial location

def parse_command(event=None):
    #counter +=1
    #print(event)
    command = game_command.get()
    if command in ['1', 'start', 'start game']:
        #start_game()
        print('Start Game')
    else:
        print("Invalid choice. Press Enter to continue...")

block = BooleanVar(game_frame, False)
# Set initial location
current_location = 'Elevator'
# Set initial counter -- CHANGE TO COUNTDOWN EVENTUALLY
counter = 0

while counter < 1000:
    current_location_data = None
    for location in locations_data['Locations']:
        if location['Name'] == current_location:
            current_location_data = location
        break

    if current_location_data:
        print(type(current_location_data))

    # Print the available directions
        available_directions = []
        for location_data in directions_data['Directions']:
            if location_data['Location'] == current_location:
                available_directions = location_data['Directions']
                break

    location_description = tk.Label(game_frame, text=current_location_data['Description'])
    location_description.pack()

    for direction_data in available_directions:
            tk.Label(game_frame,text=f"{direction_data['Direction']} - {direction_data['Destination']}").pack()
    #tk.Label.config(text=("\n".join(available_directions)))
            
    game_command = tk.Entry(game_frame)
    game_command.bind('<Return>', parse_command)
    game_command.pack()

    block.set(True)
    game_frame.wait_variable(block)
    counter += 1

if __name__ == "__main__":
    gui_window.mainloop()