import json

# Load the direction data from the JSON file
with open('directions.json', 'r') as f:
    directions_data = json.load(f)

# Initial location
current_location = 'Elevator'

while True:
    # Print the available directions
    print(f"Available directions from {current_location}:")
    available_directions = []
    for location_data in directions_data['Directions']:
        if location_data['Location'] == current_location:
            available_directions = location_data['Directions']
            break

    for direction_data in available_directions:
        print(f"{direction_data['Direction']}: {direction_data['Destination']}")

    # Get user input for the direction
    user_input = input("Enter a direction to move (or 'quit' to exit): ").strip().lower()

    # Check if the user wants to quit
    if user_input == 'quit':
        print("Exiting the game. Goodbye!")
        break

    # Check if the entered direction is valid
    valid_direction = False
    for direction_data in available_directions:
        if user_input == direction_data['Direction'].lower():
            current_location = direction_data['Destination']
            valid_direction = True
            print(f"You are now in {current_location}")
            break

    if not valid_direction:
        print("Invalid direction. Please choose a valid direction.")

