import unittest
from unittest.mock import patch, Mock
import pygame
import os
from base import SoundController

class TestSoundController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.mixer.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch('pygame.mixer.music')
    def test_volume_up(self, mock_music):
        sound_controller = SoundController()
        #sound_controller.background_music()
        mock_music.get_volume.return_value = sound_controller.current_music_volume

        sound_controller.volume_up()
        
        mock_music.set_volume.assert_called_once_with(0.4)  
                                                          # Expected volume after increasing by 0.1
        
    if __name__ == '__main__':
        unittest.main()