import unittest
import os
import pickle
from base import GameEngine

class TestGameEngine(unittest.TestCase):

    def setUp(self):
        # Initialize a GameEngine object before each test
        self.game = GameEngine()

    def test_save_game(self):
        # Given
        self.game.current_location = 'TestLocation'
        self.game.counter = 10
        self.game.player.inventory = ['testItem1', 'testItem2']
        
        # When
        self.game.save_game()
        
        # Then
        with open('saved_game.pkl', 'rb') as file:
            saved_game_state = pickle.load(file)
            
        self.assertEqual(saved_game_state['current_location'], 'TestLocation')
        self.assertEqual(saved_game_state['counter'], 10)
        self.assertListEqual(saved_game_state['inventory'], ['testItem1', 'testItem2'])

    def test_load_game(self):
        # Given
        test_state = {
            "current_location": 'LoadedLocation',
            "counter": 8,
            "inventory": ['loadedItem1', 'loadedItem2'],
            "previous_commands": [],
            "previous_locations": []
        }

        with open('saved_game.pkl', 'wb') as file:
            pickle.dump(test_state, file)

        # When
        self.game.load_game()

        # Then
        self.assertEqual(self.game.current_location, 'LoadedLocation')
        self.assertEqual(self.game.counter, 8)
        self.assertListEqual(self.game.player.inventory, ['loadedItem1', 'loadedItem2'])

    def tearDown(self):
        # Cleanup after each test by deleting the saved_game.pkl file
        try:
            os.remove('saved_game.pkl')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()

