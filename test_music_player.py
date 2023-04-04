import unittest
from unittest.mock import patch
from tkinter import Tk

import pygame.mixer

from music_player import MainApp, SONGS_DIR


class TestApp(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = MainApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_display_music(self):
        # test if the song list is displayed correctly
        expected_songs = ('song1.mp3', 'song2.mp3', 'song3.mp3')
        self.app._song_list.delete(0, 'end')
        for song in expected_songs:
            self.app._song_list.insert('end', song)
        displayed_songs = self.app._song_list.get(0, 'end')
        self.assertTupleEqual(expected_songs, displayed_songs)

    @patch('tkinter.messagebox.showerror')
    def test_play_music_with_no_song_selected(self, mock_messagebox):
        # test if an error message is displayed when no song is selected to
        # play
        self.app._song_list.selection_clear(0, 'end')
        self.app._click_play()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_play_music(self, mock_play, mock_load):
        # test if the selected song is played
        self.app._song_list.selection_clear(0, 'end')
        self.app._song_list.insert('end', 'risk-136788.mp3')
        self.app._song_list.selection_set('end')
        self.app._click_play()
        mock_load.assert_called_once_with(SONGS_DIR / 'risk-136788.mp3')
        mock_play.assert_called_once_with()

    @patch('pygame.mixer.music.pause')
    def test_pause_music(self, mock_pause):
        # test if the playing music is paused
        self.app._song_list.selection_clear(0, 'end')
        self.app._song_list.insert('end', 'risk-136788.mp3')
        self.app._song_list.selection_set('end')
        self.app._click_play()
        self.app._click_pause()
        mock_pause.assert_called_once_with()

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_no_song_selected(self, mock_messagebox):
        # test if an error message is displayed when no song is selected to
        # pause
        self.app._song_list.selection_clear(0, 'end')
        self.app._click_pause()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')


