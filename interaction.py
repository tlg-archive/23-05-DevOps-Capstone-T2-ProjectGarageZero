import json
import random

# Try to load data from the external file 'npcdata.json'
try:
    with open('npcdata.json', 'r') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error loading JSON data: {e}")
    exit()

def get_random_greeting(npc_name):
    for npc in data['NPCs']:
        if npc['Name'] == npc_name:
            if npc_name == "Attendant":
                return random.choice(npc['Greetings'])
            elif npc_name == "Creepy Man":
                for choice in npc['PlayerChoices']:
                    if choice['Choice'] == "Hello, have you seen a grey Mazda?":
                        return random.choice(choice['ResponseOptions'])
    return None  # Returns None if the npc_name doesn't match any NPCs in the data

# Testing the functions
print(get_random_greeting("Attendant"))  # Get a random greeting from the Attendant
print(get_random_greeting("Creepy Man"))  # Get a random response option from Creepy Man

