import json

# Load the direction data from the JSON file
with open('directions.json', 'r') as f:
    directions_data = json.load(f)

# Initial location
current_location = 'Elevator'

while True:
    # Print the available directions
    print(f"Available directions from {current_location}:")
    available_directions = directions_data['Directions'][current_location]
    for direction, destination in available_directions.items():
        print(f"{direction}: {destination}")

    # Get user input for the direction
    user_input = input("Enter a direction to move (or 'quit' to exit): ").strip().lower()

    # Check if the user wants to quit
    if user_input == 'quit':
        print("Exiting the game. Goodbye!")
        break

    # Check if the entered direction is valid
    if user_input in available_directions:
        current_location = available_directions[user_input]
        print(f"You are now in {current_location}")
    else:
        print("Invalid direction. Please choose a valid direction.")
