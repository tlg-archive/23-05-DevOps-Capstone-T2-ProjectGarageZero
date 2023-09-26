import unittest
from unittest.mock import patch
import pygame
import io
from base import GameCommand,game_text
import sys

class TestDisplayHelp(unittest.TestCase):
    def setUp(self):
        self.game = GameCommand()

    def test_display_help(self):
        self.maxDiff = None 
        expected_output = game_text['help'] + "\n"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.game.display_help()
            actual_output =mock_stdout.getvalue()

        self.assertEqual(actual_output, expected_output)


"""class TestGreetFunction(unittest.TestCase): 

    def setUp(self): 

        # Redirect sys.stdout to capture the printed output 

        self.saved_stdout = sys.stdout 

        sys.stdout = io.StringIO() 
        self.game = GameCommand()

    def tearDown(self): 

        # Restore sys.stdout to its original value 

        sys.stdout = self.saved_stdout 

    def test_display_help(self): 
        self.maxDiff = None 
        # Call the function with a specific name 

        self.game.display_help()
        # Capture the printed output from sys.stdout 

        printed_output = sys.stdout.getvalue() 
        # Assert that the printed output matches the expected message 

        expected_output = game_text['help'] + "\n"

        self.assertEqual(printed_output, expected_output)"""

if __name__ == '__main__':
    unittest.main()

    
        