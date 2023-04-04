import time
import tkinter as tk
from music_player import MainApp
import pygame


def test_main_app():

    # create main app
    root = tk.Tk()
    app = MainApp(root)

    # test GUI initialization
    assert isinstance(app._song_list, tk.Listbox)
    assert isinstance(app._buttons_frame, tk.Frame)

    # test music functions
    # play a song
    app._click_play()
    assert pygame.mixer.music.get_busy()
    time.sleep(5)

    # pause the song
    app._click_pause()
    assert not pygame.mixer.music.get_busy()

    # unpause the song
    app._click_play()
    assert pygame.mixer.music.get_busy()
    time.sleep(5)

    # stop the song
    app._click_pause()
    assert not pygame.mixer.music.get_busy()

    root.destroy()


if __name__ == "__main__":
    test_main_app()
