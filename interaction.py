import json
import random

# Load data from the external file 'npcdata.json'
def load_data():
    try:
        with open('data/npcdata.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        exit()

data = load_data()

def get_npc(npc_name):
    for npc in data['NPCs']:
        if npc['Name'] == npc_name:
            return npc
    return None

def greet_npc(npc):
    if 'Greetings' in npc:
        return random.choice(npc['Greetings'])
    return None

def interact_with_npc(npc):
    print(greet_npc(npc))
    
    if 'PlayerChoices' in npc:
        while True:  # This loop allows the player to keep choosing until they decide to exit
            for idx, choice in enumerate(npc['PlayerChoices']):
                print(f"{idx + 1}. {choice['Choice']}")

            # Add an option to exit the conversation
            exit_option_index = len(npc['PlayerChoices']) + 1
            print(f"{exit_option_index}. Exit conversation")

            player_choice = input("Choose an option (type the number): ")

            try:
                choice_index = int(player_choice) - 1
                if 0 <= choice_index < len(npc['PlayerChoices']):
                    if 'Response' in npc['PlayerChoices'][choice_index]:
                        response = npc['PlayerChoices'][choice_index]['Response']
                    elif 'ResponseOptions' in npc['PlayerChoices'][choice_index]:
                        response = random.choice(npc['PlayerChoices'][choice_index]['ResponseOptions'])
                    else:
                        response = "No response found."
                    print(response)
                elif choice_index + 1 == exit_option_index:  # Exit conversation
                    print("Exiting conversation.")
                    return  # This returns the player to the main command input
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid choice.")

def main():
    while True:
        command = input("Enter a command (or type 'exit' to quit): ")

        # Quit the game
        if command.lower() == "exit":
            print("Goodbye!")
            break
        
        # If command starts with "Talk"
        elif command.lower().startswith("talk "):
            npc_name = command[5:]  # Extract the name of the NPC after the word 'Talk'
            npc = get_npc(npc_name)
            if npc:
                interact_with_npc(npc)
            else:
                print(f"No NPC named {npc_name} found.")

        else:
            print("Invalid command.")

if __name__ == "__interaction__":
    main()

