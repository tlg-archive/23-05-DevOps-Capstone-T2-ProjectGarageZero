import unittest
import functionsTest
from functionsTest import get_item, items_data, drop_item, look_at_item  # Import your game module
from refactor import Player, SoundController, TextParser

#ADD TESTS FROM REFACTOR.PY BELOW

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

if __name__ == '__main__':
    unittest.main()