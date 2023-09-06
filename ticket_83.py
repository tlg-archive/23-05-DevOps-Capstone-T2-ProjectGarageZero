import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_splash_screen():
    clear_screen()
    print("============================================")
    print("          Project Garage Zero:               ")
    print("       The Apprentice's Dilemma             ")
    print("============================================")
    input("Press Enter to continue...")
    clear_screen()

