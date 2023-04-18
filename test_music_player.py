"""
Tests methods in MainApp classes in music_player.py
"""

import unittest
from unittest.mock import patch, Mock, call
import tkinter as tk
from music_player import MainApp, SONGS_DIR


class TestApp(unittest.TestCase):

    def setUp(self):
        """set root and app"""
        self.root = tk.Tk()
        self.app = MainApp(self.root)

    def tearDown(self):
        """destroy all the widgets and exit mainloop"""
        self.root.destroy()

    def test_load_images(self) -> None:
        """test if images' format are changed to tk.PhotoImage"""
        img_dict = self.app.load_images()
        self.assertIsInstance(img_dict, dict)
        self.assertEqual(len(img_dict), 6)
        for img in img_dict.values():
            self.assertIsInstance(img, tk.PhotoImage)

    def test_add_music(self):
        """test if music can be added"""
        # create a mock file dialog
        mock_file_dialog = Mock()
        mock_file_dialog.return_value = 'lifelike.mp3'
        # patch the filedialog.askopenfilename method to use the mock file
        # dialog
        with patch('tkinter.filedialog.askopenfilename', new=mock_file_dialog):
            # simulate clicking on the "add" button
            self.app.click_add()
        # check that the song was added to the song list
        song_list = self.app.playlist.get(0, tk.END)
        self.assertIn('lifelike.mp3', song_list)

    @patch('tkinter.messagebox.showerror')
    def test_click_add_duplicate_song(self, mock_messagebox):
        """test if error message will pop up after adding duplicated song"""
        # set up the test by adding a song to the song_list
        self.app.playlist.insert(tk.END, 'drop-it.mp3')
        # create a mock file dialog
        mock_file_dialog = Mock()
        mock_file_dialog.return_value = 'drop-it.mp3'
        # patch the filedialog.askopenfilename method to use the mock file
        # dialog
        with patch('tkinter.filedialog.askopenfilename', new=mock_file_dialog):
            self.app.click_add(attempts=3)

        mock_messagebox.assert_has_calls([
            call('show error', 'the song is already added!'),
            call('show error', 'too many attempts to add a duplicated song!')
        ])

    @patch('tkinter.messagebox.showerror')
    def test_play_music_with_no_song_selected(self, mock_messagebox):
        """"test if an error message is displayed when no song is selected to
        play"""
        self.app.playlist.selection_clear(0, 'end')
        self.app.click_play()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_play_music(self, mock_play, mock_load):
        """test if the selected song is played"""
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.selection_set('end')
        self.app.click_play()
        mock_load.assert_called_once_with(SONGS_DIR / 'risk.mp3')
        mock_play.assert_called_once_with()

    @patch('pygame.mixer.music.pause')
    def test_pause_music(self, mock_pause):
        """test if the playing music is paused"""
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.selection_set('end')
        self.app.click_play()
        self.app.click_pause()
        mock_pause.assert_called_once_with()

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_no_song_selected(self, mock_messagebox):
        """test if an error message is displayed when no song is selected to
        pause"""
        self.app.playlist.selection_clear(0, 'end')
        self.app.click_pause()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_no_song_playing(self, mock_messagebox):
        """Ensure that an error message is displayed when no song is playing"""
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.selection_set('end')
        self.app.click_play()
        self.app.click_pause()
        self.app.click_pause()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song is playing!')

    @patch('tkinter.messagebox.showerror')
    def test_pause_music_with_selected_song_not_playing(self, mock_messagebox):
        """Ensure that an error message is displayed when selected song is not
        playing"""
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.selection_set('end')
        self.app.click_play()
        self.app.playlist.insert('end', 'drop-it.mp3')
        self.app.playlist.selection_set('end')
        self.app.playlist.activate('end')
        self.app.click_pause()
        mock_messagebox.assert_called_once_with(
            'show error',
            'the selected song is not playing!')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_click_next(self, mock_play, mock_load):
        """test if next song is played"""
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.insert('end', 'drop-it.mp3')
        self.app.playlist.selection_set(0)
        self.app.playlist.activate(0)
        self.app.click_next()

        mock_load.assert_called_once_with(SONGS_DIR / 'drop-it.mp3')
        mock_play.assert_called_once_with()

    @patch('tkinter.messagebox.showerror')
    def test_click_next_with_no_song_selected(self, mock_messagebox):
        """"test if an error message is displayed when no song is selected to
        play"""
        self.app.playlist.selection_clear(0, 'end')
        self.app.click_next()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_click_prev(self, mock_play, mock_load):
        """test if previous song is played"""
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.insert('end', 'drop-it.mp3')
        self.app.playlist.selection_set(0)
        self.app.playlist.activate(0)
        self.app.click_prev()

        mock_load.assert_called_once_with(SONGS_DIR / 'drop-it.mp3')
        mock_play.assert_called_once_with()

    @patch('tkinter.messagebox.showerror')
    def test_click_prev_with_no_song_selected(self, mock_messagebox):
        """"test if an error message is displayed when no song is selected to
        play"""
        self.app.playlist.selection_clear(0, 'end')
        self.app.click_prev()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')

    def test_click_delete(self):
        """test if the song is deleted"""
        # add a song
        self.app.playlist.insert('end', 'risk.mp3')
        self.app.playlist.selection_set('end')
        self.app.playlist.activate('end')
        # check if song is added to the listbox
        assert self.app.playlist.size() == 1
        # delete the song
        self.app.click_delete()
        # check if listbox is empty
        assert self.app.playlist.size() == 0

    @patch('tkinter.messagebox.showerror')
    def test_click_delete_with_no_song_selected(self, mock_messagebox):
        """Ensure that an error message is displayed when no song is
        selected"""
        self.app.playlist.selection_clear(0, 'end')
        self.app.click_delete()
        mock_messagebox.assert_called_once_with('show error',
                                                'no song selected!')


if __name__ == '__main__':
    unittest.main()