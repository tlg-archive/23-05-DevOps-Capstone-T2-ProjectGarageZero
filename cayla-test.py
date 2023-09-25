import unittest
import functionsTest
from functionsTest import get_item, items_data, drop_item, look_at_item  # Import your game module

class TestGame(unittest.TestCase):
    def setUp(self):
        #Create a new game instance for each test
        functionsTest.inventory = []
        functionsTest.current_location = 'Elevator'
        functionsTest.items_data = items_data

    def test_get_item(self):
        added_item = "gum"
        new_inventory = ["gum"]
        # When
        get_item(added_item,functionsTest.current_location)
        # Then
        assert new_inventory == functionsTest.inventory

#START GAME
#EAIT FORT USER IMPIT (or test input)
#check if response is correct
#end loop

if __name__ == '__main__':
    unittest.main()