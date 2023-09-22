"""
PRE TEXT PARSER VERSION OF MAIN-GUI FOR ORIGINAL GUI GAME LOGIC REFERENCE
"""

import tkinter as tk
import os
import json
from tkinter import Frame, messagebox
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
    messagebox.showinfo("showinfo", game_text["help"])


#MENUBAR
menubar = tk.Menu(gui_window)
gui_window.config(menu=menubar)

#HELP
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Help", command=display_help)

menubar.add_cascade(menu=help_menu, label="Help")

#ALL frame
title_frame = Frame(gui_window)
title_frame.pack()

game_frame = Frame(gui_window)

#TITLE FRAME label settings
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
    update_game_text()
    # Set initial location

# Set initial location
current_location = 'Elevator'
# Set initial counter -- CHANGE TO COUNTDOWN EVENTUALLY
counter = 0

output_text = tk.Label(game_frame)
output_text.pack()

choices_frame = Frame(game_frame)
choices_frame.pack()

#POPULATE GLOBAL VARIABLES WITH CURRENT LOCATION AND DIRECTIONS DATA
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
    return [new_location_data, current_directions]

#CLEAR THE CHOICES FRAME TO DISPLAY THE NEW EXIT OPTIONS FOR THE NEXT ROOM
def clear_choices():
    #print(' I AM IN THE FUNCGIOJTR')
    #print(f"children in choices frame: {choices_frame.winfo_children()}")
    for widget in choices_frame.winfo_children():
        #print(' I AM IN THE LOPPP FSIFHNALSCNSAL', widget)
        widget.destroy()
    

# Function to update the game text
def update_game_text():
    #GET THE UPDATED LOCATION DATA
    #print("LOCATIONS DATA",current_location_data)
    current_location_data, available_directions = get_location_data()
    #available_directions = get_location_data()[1]
    output_text.configure(text=current_location_data["Description"])

    for direction_data in available_directions:
        tk.Label(choices_frame,text=f"{direction_data['Direction']} - {direction_data['Destination']}").pack()

#TESTING TO SEE IF GLOBAL VARIABLES RELATING TO LOCATION UPDATE
def test_location():
    print(f"NEW CURRENT LOCATION:{current_location}")
    current_location_data = get_location_data()[0]
    available_directions = get_location_data()[1]
    print("LOCATIONS DATA",current_location_data)
    print("DIRECTIONS DATA",available_directions)


# Function to handle user input
def process_input(event=None):
    global current_location  # Declare current_location as global
    global current_location_data
    global available_directions
    user_input = game_command.get().strip()
    #game_command.delete(0, tk.END)

    current_location_data = get_location_data()[0]
    #print(f"user input: {user_input}")
    #print(f"user input: {current_location_data}")
    
    #CHECK IF THE USER INPUT IS EQUAL TO THE DIRECTION OPTIONS OF THIS LOCATION
    if user_input.title() in current_location_data["Directions"]:
        choice = user_input.title()
        current_location = current_location_data["Directions"][choice]
        #print(f'CURRENT LOCATION: {current_location}')
        #test_location()
        clear_choices()
        update_game_text()
    else:
        print( "Invalid choice. Try again")

game_command = tk.Entry(game_frame)
game_command.bind('<Return>', process_input)
game_command.pack()

if __name__ == "__main__":
    gui_window.mainloop()