import tkinter as tk
import os
import json

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

#general label settings
title_label = tk.Label(root, text=game_text["title"])
title_label.pack()

#display the window
#root.mainloop()

def choose_start():
    command = command_line.get()
    if command in ['1', 'start', 'start game']:
        #start_game()
        print('Start Game')
    elif command in ['2', 'quit', 'exit']:
        #clear_screen()
        print("Goodbye!\n")
        #sys.exit()
    else:
        print("Invalid choice. Press Enter to continue...")


#example text input
command_line = tk.Entry(root)
command_line.pack()

#example button
start_button = tk.Button(root, text="Start Game", command = choose_start)
start_button.pack()

if __name__ == "__main__":
    root.mainloop()