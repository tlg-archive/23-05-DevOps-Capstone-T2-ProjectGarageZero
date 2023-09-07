import json

# Load the direction data from the JSON file
with open('directions.json', 'r') as f:
    directions_data = json.load(f)

# Load location data from the JSON file
with open('locations.json', 'r') as f:
    locations_data = json.load(f)

# Initial location
current_location = 'Elevator'

while True:
    # Print the current location
    print(f"LOCATION: {current_location}")

    # Get and print the current location's description
    current_location_data = current_location
    for location in locations_data['Locations']:
        if location['Name'] == current_location:
            current_location_data = location
            break

    if current_location_data:
        print(f"(Location Description Prints Here) {current_location_data['DescriptionID']}") #NOT PRINTING DESC FROM VAR

    # Print the available directions
    print(f"EXITS:")
    available_directions = []
    for location_data in directions_data['Directions']:
        if location_data['Location'] == current_location:
            available_directions = location_data['Directions']
            break

    for direction_data in available_directions:
        print(f"{direction_data['Direction']} -  {direction_data['Destination']}")

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
