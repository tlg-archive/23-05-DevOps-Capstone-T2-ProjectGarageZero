import tkinter as tk
import os
import json
from tkinter import Frame

#helper functions
script_dir = os.path.dirname(os.path.realpath(__file__))
text_file = os.path.join(script_dir, 'data', 'game-text.json')

def convert_json():
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text
game_text = convert_json()

#initilize the tkinter window and size
root = tk.Tk()
#root.geometry("500x500")

#title frame
title_frame = Frame(root)
title_frame.pack()

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

def start_game():
    game_frame = Frame(root)
    print("yey")


#example text input
command_line = tk.Entry(title_frame)
command_line.bind('<Return>', choose_start)
command_line.pack()

#example button
start_button = tk.Button(title_frame, text="Start Game", command = choose_start)
start_button.pack()

if __name__ == "__main__":
    root.mainloop()