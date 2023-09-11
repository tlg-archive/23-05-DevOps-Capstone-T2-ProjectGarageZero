import json
from mapidea import display_map

# Load direction data from the JSON file
with open('directions.json', 'r') as f:
    directions_data = json.load(f)

# Load location data from the JSON file
with open('locations.json', 'r') as f:
    locations_data = json.load(f)

# Load description data from the JSON file
with open('descriptions.json', 'r') as f:
    descriptions_data = json.load(f)

# start game function defined but not auto-run when file imports
def start_game():

    # Set initial location
    current_location = 'Elevator'
    # Set initial counter -- CHANGE TO COUNTDOWN EVENTUALLY
    counter = 0

    while True:
        # Print the current location
        print(f"LOCATION: {current_location}")

        # Print current # of moves made, increment up for next loop -- CHANGE TO COUNTDOWN EVENTUALLY
        print(f"MOVES MADE: {counter}\n")
        counter += 1

        # Get and print the current location's description
        current_location_data = None
        for location in locations_data['Locations']:
            if location['Name'] == current_location:
                current_location_data = location
                break

        if current_location_data:
            print(f"{current_location_data['Description']}\n") 

        # Print the available directions
        print(f"EXITS:")
        available_directions = []
        for location_data in directions_data['Directions']:
            if location_data['Location'] == current_location:
                available_directions = location_data['Directions']
                break

        for direction_data in available_directions:
            print(f"{direction_data['Direction']} - {direction_data['Destination']}\n")

        # Get user input for the direction
        user_input = input("Enter a direction to move (e.g., 'go north') or 'quit' to exit:\n\n").strip().lower()

        # Check if the user wants to quit
        if user_input == 'quit':
            print("Exiting the game. Goodbye!")
            break

        if user_input == 'help':
            print("\n------HELP SCREEN------")
            print("\nTo move, type a valid command. For example, 'go south' will move you one place south.")
            print("Game Layout")
            print("_____________________________________")
            print(f"Current Location: Displayed in the top left")
            print(f"Moves you've taken: Displayed below")
            print(f"Description of your location: You will see the description of your current location")
            print("Your nearest exits: The places you can move to")
            print("_____________________________________")
            print("Below is a map of the game:")
            display_map()  # Call the display_map() function to show the map
            continue

        # Check if the user requests the map directly
        if user_input == 'map':
            display_map()
            continue

        # Split the user input into words
        words = user_input.split()

        if len(words) < 2:
            print("Please include both a verb and a direction (e.g., 'go north').")
            continue

        verb, direction = words[0], " ".join(words[1:])

        # Check if the entered direction is valid
        valid_direction = False
        for direction_data in available_directions:
            if direction == direction_data['Direction'].lower() and verb == 'go':
                current_location = direction_data['Destination']
                valid_direction = True
                # SAMMY: Remarked out because redundant with Location Header
                #print(f"You are now in {current_location}")
                break

        if not valid_direction:
            print("Invalid direction. Please choose a valid direction.")

# This block ensures that the code inside start_game() is only executed when
# this script is run as the main program
if __name__ == "__main__":
    start_game()
