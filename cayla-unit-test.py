import unittest
from base import Player,GameEngine, items_data

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.new_game = GameEngine()

    def test_get_item(self):
        added_item = "gum"
        #new_inventory = ["gum"]
        # When
        self.player.get_item(added_item)
        # Then
        self.assertIn("gum", self.player.inventory)

    def test_drop_item(self):
        dropped_item = "gum"
        current_location = 'Elevator'

        self.player.get_item(dropped_item)

        self.player.drop_item(dropped_item, current_location)
        self.assertNotIn('gum', self.player.inventory)

if __name__ == "__main__":
    unittest.main()