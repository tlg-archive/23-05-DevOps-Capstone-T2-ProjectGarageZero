import json
import os

# Load data from JSON files once at the beginning
with open('locations.json', 'r') as f:
	locations_data = json.load(f)

with open('items.json', 'r') as f:
	items_data = json.load(f)

with open('directions.json', 'r') as f:
	directions_data = json.load(f)

with open('descriptions.json', 'r') as f:
	descriptions_data = json.load(f)

# Define your classes here
class Location:
	# ... (same as before)

class Item:
	# ... (same as before)

# Create instances of your classes based on the loaded data
locations = []
for loc_data in locations_data['Locations']:
	# ... (same as before)

items = []
for item_data in items_data['Items']:
	# ... (same as before)

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def display_splash_screen():
	# ... (same as before)

def move_player():
	current_location = 'Elevator'
	while True:
		# ... (same as before)

def new_game():
	clear_screen()
	print("Game has started!")
	move_player()

def main_game_loop():
	while True:
		clear_screen()
		# ... (same as before)
		if choice == '1':
			new_game()
		elif choice == '2':
			clear_screen()
			print("Goodbye!")
			break
		else:
			input("Invalid choice. Press Enter to continue...")

if __name__ == "__main__":
	display_splash_screen()
	main_game_loop()

