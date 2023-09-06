map_visual = [
    "Elevator [E]",
    "   |",
    "   |",
    "   V",
    "Parking West 1 [PW1] <--- > Parking East 1 [PE1]",
    "   ^               ^         ^",
    "   |               |         |",
    "   V               V         V",
    "Parking West 2 [PW2] <--- > Parking East 2 [PE2]",
    "   ^               ^         ^",
    "   |               |         |",
    "   V               V         V",
    "Parking West 3 [PW3] <--- > Parking East 3 [PE3]",
    "                                  ^",
    "                                  |",
    "                                  V",
    "                               Exit [X]"
]

# Example function to display the map with the current location highlighted
def display_map(current_location):
    location_symbols = {
        "elevator": "[E]",
        "parking_west_1": "[PW1]",
        "parking_west_2": "[PW2]",
        "parking_west_3": "[PW3]",
        "parking_east_1": "[PE1]",
        "parking_east_2": "[PE2]",
        "parking_east_3": "[PE3]",
        "exit": "[X]"
    }
    
    for line in map_visual:
        if location_symbols[current_location] in line:
            print(">" + line)
        else:
            print(" " + line)

# Test
display_map("parking_east_2")

