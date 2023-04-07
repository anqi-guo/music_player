import unittest
from unittest.mock import patch
import tkinter as tk

from music_player import MainApp, SONGS_DIR


class TestApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MainApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_load_images(self) -> None:
        img_dict = self.app.load_images()
        self.assertIsInstance(img_dict, dict)
        self.assertEqual(len(img_dict), 6)
        for img in img_dict.values():
            self.assertIsInstance(img, tk.PhotoImage)

    def test_add_music(self):
        # test if music can be added to the listbox
        # check if listbox is empty
        assert self.app.song_list.size() == 0
        # add a song to the listbox
        self.app.click_add()
        # check if song is added to the listbox
        assert self.app.song_list.size() == 1

    @patch('tkinter.messagebox.showerror')
    def test_add_duplicated_music(self, mock_messagebox):
        # test adding music that is already in the song list
        # add a random song
        self.app.click_add()
        # add that song one more time
        self.app.click_add()
        mock_messagebox.assert_called_once_with('show error',
                                                'the song is already added!')

    @patch('tkinter.messagebox.showerror')
    def test_play_music_with_no_song_selected(self, mock_messagebox):
        # test if an error message is displayed when no song is selected to
        # play
        self.app.song_list.selection_clear(0, 'end')
        self.app.click_play()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_play_music(self, mock_play, mock_load):
        # test if the selected song is played
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.selection_set('end')
        self.app.click_play()
        mock_load.assert_called_once_with(SONGS_DIR / 'risk.mp3')
        mock_play.assert_called_once_with()

    @patch('pygame.mixer.music.pause')
    def test_pause_music(self, mock_pause):
        # test if the playing music is paused
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.selection_set('end')
        self.app.click_play()
        self.app.click_pause()
        mock_pause.assert_called_once_with()

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_no_song_selected(self, mock_messagebox):
        # test if an error message is displayed when no song is selected to
        # pause
        self.app.song_list.selection_clear(0, 'end')
        self.app.click_pause()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_no_song_playing(self, mock_messagebox):
        # Ensure that an error message is displayed when no song is playing
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.selection_set('end')
        self.app.click_play()
        self.app.click_pause()
        self.app.click_pause()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song is playing!')

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_selected_song_not_playing(self, mock_messagebox):
        # Ensure that an error message is displayed when selected song is not
        # playing
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.selection_set('end')
        self.app.click_play()
        self.app.song_list.insert('end', 'drop-it.mp3')
        self.app.song_list.selection_set('end')
        self.app.song_list.activate('end')
        self.app.click_pause()
        mock_messagebox.assert_called_once_with(
            'show error',
            'the selected song is not playing!')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_click_next(self, mock_play, mock_load):
        # test if next song is played
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.insert('end', 'drop-it.mp3')
        self.app.song_list.selection_set(0)
        self.app.song_list.activate(0)
        self.app.click_next()

        mock_load.assert_called_once_with(SONGS_DIR / 'drop-it.mp3')
        mock_play.assert_called_once_with()

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_click_prev(self, mock_play, mock_load):
        # test if previous song is played
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.insert('end', 'drop-it.mp3')
        self.app.song_list.selection_set(0)
        self.app.song_list.activate(0)
        self.app.click_prev()

        mock_load.assert_called_once_with(SONGS_DIR / 'drop-it.mp3')
        mock_play.assert_called_once_with()

    def test_click_delete(self):
        # test if the song is deleted
        # add a song
        self.app.song_list.insert('end', 'risk.mp3')
        self.app.song_list.selection_set('end')
        self.app.song_list.activate('end')
        # check if song is added to the listbox
        assert self.app.song_list.size() == 1
        # delete the song
        self.app.click_delete()
        # check if listbox is empty
        assert self.app.song_list.size() == 0

    @patch('tkinter.messagebox.showerror')
    def test_click_delete_with_no_song_selected(self, mock_messagebox):
        # Ensure that an error message is displayed when no song is
        self.app.click_delete()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')


