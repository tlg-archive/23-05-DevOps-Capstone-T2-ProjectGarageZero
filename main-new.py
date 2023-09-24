import os
import sys
#Suppressing Pygame support prompt that was displaying pre-splash screen
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import textwrap
#from ticket_83 import *
from refactor import *

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, width=50):
    wrapped_text = textwrap.fill(text, width=30)  # Setting width to 30 characters as per your request
    for line in wrapped_text.split('\n'):
        print(line.center(width))
    print()  # Print an additional newline for spacing

def display_splash_screen():
    clear_screen()
    print_centered("==============================")
    print_centered("Project Garage Zero:")
    print_centered("The Apprentice's Dilemma")
    print_centered("==============================")
    input("\n\nPress Enter to continue...")
    clear_screen()

    print_centered("STORY:")
    print_centered("You are a young, bright-eyed individual, striving to become the next DevOps Engineer at MSM. You have just left your interview...")
    print_centered("...and you can't remember where you parked your car!")
    print_centered("You have a validated ticket but there's limited time before you have to pay extra for parking.")
    input("\n\nPress Enter to continue...")
    clear_screen()

    print_centered("OBJECTIVE:")
    print_centered("Find your car and leave the garage without paying an additional fee.")
    print_centered("HOW TO WIN:")
    print_centered("Locate your car and reach the garage exit before the step counter runs out.")
    input("\n\nPress Enter to continue...")
    clear_screen()

def main_game_loop():
    display_splash_screen()
    while True:
        clear_screen()
        print("Welcome to Project Garage Zero: The Apprentice's Dilemma!\n")
        print("1. Start a New Game")
        print("2. Quit")
        choice = input("\n> ")
        if choice == '1':
            new_game.play_game()
        elif choice == '2':
            clear_screen()
            print("Goodbye!\n")
            sys.exit()
        else:
            input("Invalid choice. Press Enter to continue...")

# Define your functions for game logic here
# SAMMY: MOVING UP FOR CODE EXECUTION TO KEEP IT FIRST
if __name__ == '__main__':
    main_game_loop()