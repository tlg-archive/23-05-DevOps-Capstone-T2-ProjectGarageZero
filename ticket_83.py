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

    print("Story:")
    print("You are trying to become an apprentice for MSM and you have just left your interview.")
    print("But there's one problem: you can't remember where you parked your car!")
    print("You have a validated ticket but there's limited time before you have to pay extra for parking.")
    input("Press Enter to continue...")
    clear_screen()

    print("Objective:")
    print("Before the step counter runs out, you need to find your car and leave the garage.")
    print("Face different obstacles on your quest to exit and avoid paying the additional parking fee.")
    input("Press Enter to continue...")
    clear_screen()

    print("Player:")
    print("You are a young, bright-eyed individual, striving to become the next DevOps Engineer at MSM.")
    input("Press Enter to continue...")
    clear_screen()

    print("How to Win:")
    print("Reach the garage exit and locate your car before the step counter runs out.")
    input("Press Enter to continue...")
    clear_screen()

    print("Player is presented with the option to play a New Game.")
    input("Press Enter to start a New Game...")

def main_game_loop():
    #display_splash_screen()
    while True:
        clear_screen()
        print("Welcome to Project Garage Zero: The Apprentice's Dilemma!")
        print("1. Start a New Game")
        print("2. Quit")
        choice = input("> ")
        if choice == '1':
            # Start a new game
            new_game()
        elif choice == '2':
            clear_screen()
            print("Goodbye!")
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def new_game():
    clear_screen()
    print("Game has started!")
    # Game logic will go here
    while True:
        action = input("> ").strip()
        if action.lower() == "quit":
            break
        # Handle game-specific commands and logic here

if __name__ == "__main__":
    main_game_loop()
