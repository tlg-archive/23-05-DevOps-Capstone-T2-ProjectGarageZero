# Updated map_visual with items in each SECTION
map_visual = [
    "Elevator [E]",
    "   |",
    "   |",
    "   V",
    "Parking West 1 [PW1] <--- > Parking East 1 [PE1]",
    "   ^                         ^",
    "   |                         |",
    "   V                         V",
    "Parking West 2 [PW2] <--- > Parking East 2 [PE2]",
    "   ^                         ^",
    "   |                         |",
    "   V                         V",
    "Parking West 3 [PW3] <--- > Parking East 3 [PE3]",
    "                                  ^",
    "                                  |",
    "                                  V",
    "                               Exit [X]"
]

# Dictionary to store items in each section
section_items = {
    "elevator": ["Garbage can", "Pack of gum"],
    "parking_west_1": [],
    "parking_west_2": ["Mazda", "Mouse"],
    "parking_west_3": [],
    "parking_east_1": ["Tesla", "Puddle", "Light"],
    "parking_east_2": ["Creepy Man", "Lollipop", "Newspaper"],
    "parking_east_3": [],
    "exit": ["Attendant"]
}

# Dictionary to store descriptions for items, locations, and NPCs
descriptions = {
    "Garbage can": "A greyidh greem garabage can placed near the elevstor, it id only hlaf full but mostly filled with reciepts.",
    "Pack of gum": "A black snf blue metsllic psck of gum rest on the floor prctically new and untouched.",
    "Mazda": "A dark grey Mazda CX-3 clearly in need of a good wash.",
    "Mouse": "A small brown mouse is perched ontop of the side mirror stopping you from entering the car.",
    "Tesla": "A blue tesla psrked nicely in its own spot slowly being consumed by the puddle next to it.",
    "Puddle": "A puddle slowly growing in size from a leaking pipe. With every drop of water from the leak the puddle consumes more of the parking area.",
    "Light": "A bright light fixture over the parking area reflexing off the puddle and the tesla, the light highlighting what you can afford one day if you are successful at this apprenticeship",
    "Creepy Man": "He wore a long, worn leather jacket that reached down to his ankles, and a wide-brimmed hat pulled low, obscuring most of his face. The shadow cast by his hat concealed his eyes, adding an air of mystery and unease..",
    "Lollipop": "The loolipop has a bright yellow ans pink wrapping, you cannot tell the flavor based purely on the wrapper.",
    "Newspaper": "A newspaper has smeared ink, you cannot tell how old the paper is. It is clearly just garbage.",
    "Attendant": "A young women sitting in a parking booth was scrolling on her phone to pass the time as she waits for people to leave the parking lot."
}

# Example function to display the map with items and the current location highlighted
def display_map_with_items(current_location):
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
    
    current_section = None
    for section, symbol in location_symbols.items():
        if symbol in current_location:
            current_section = section
            break
    
    for line in map_visual:
        if location_symbols[current_location] in line:
            print(">" + line)
        elif current_section and location_symbols[current_section] in line:
            item_list = section_items[current_section]
            if item_list:
                items = ", ".join(item_list)
                print(" " + line + f" ({items})")
            else:
                print(" " + line)
        else:
            print(" " + line)

# Function to look at an item, location, or NPC and display its description
def look_command(input_text):
    parts = input_text.split()
    
    if len(parts) < 2:
        print("Please specify what you want to look at.")
    else:
        item_name = " ".join(parts[1:])
        if item_name in descriptions:
            print(descriptions[item_name])
        else:
            print(f"You don't see {item_name} here.")

# Test
display_map_with_items("elevator")

# Test the "Look" command
look_command("Look Garbage can")
look_command("Look Tesla")
look_command("Look Nonexistent Item")
