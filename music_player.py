import tkinter as tk
from tkinter import messagebox
import pygame
from pathlib import Path
from typing import Dict

SONGS_DIR = Path('audio')
IMAGE_DIR = Path('logo')


class MainApp:
    def __init__(self, parent):
        self._parent = parent
        self._images = self._load_images()
        self._current_song = None
        self._paused = False
        self._init_ui()
        pygame.init()

    def _init_ui(self):
        self._song_list = tk.Listbox(self._parent,
            bg='black', fg='white', height=25, width=55)
        self._song_list.grid(row=0, column=0)

        self._buttons_frame = tk.Frame(self._parent)
        self._buttons_frame.grid(row=1, column=0)

        button_dict = {
            'prev': [1, self._click_prev],
            'play': [2, self._click_play],
            'pause': [3, self._click_pause],
            'next': [4, self._click_next],
            'trash': [5, self._click_delete]
        }

        for name, (row, callback) in button_dict.items():
            tk.Button(self._buttons_frame, image=self._images[name], command=callback) \
                .grid(row=0, column=row, padx=10, pady=10)

        self._display_music()

    def _load_images(self) -> Dict[str, tk.PhotoImage]:
        img_names = ['play', 'pause', 'next', 'prev', 'trash']
        img_dict = {}
        for name in img_names:
            img_dict[name] = tk.PhotoImage(file= IMAGE_DIR / f'{name}.png')
        return img_dict

    def _display_music(self):
        # display songs to the song_list
        for song in SONGS_DIR.glob('*.mp3'):
            self._song_list.insert(tk.END, song.name)
        # clear song box
        self._song_list.selection_clear(0, tk.END)
        # activate first song
        self._song_list.activate(0)
        # select first song
        self._song_list.selection_set(0)

    def _click_play(self):
        # check if a song is selected
        if self._song_list.curselection() == ():
            messagebox.showerror('show error', 'no song selected!')
        # if the song paused is same as the song selected
        # then unpause the song and update paused to False
        elif self._current_song == self._song_list.get(tk.ACTIVE) and self._paused:
            self._unpause_music()
        # otherwise, just play the song selected
        # and update the current song to the song selected
        else:
            self._play_music()

    def _click_pause(self):
        # if no song is selected
        if self._song_list.curselection() == ():
            messagebox.showerror('show error', 'no song selected!')
        # if no song is playing
        elif self._paused is True:
            messagebox.showerror('show error', 'no song is playing')
        # if a song is selected but the selected song is different from the
        # song playing
        elif self._current_song != self._song_list.get(tk.ACTIVE):
            messagebox.showerror('show error',
                                 'the selected song is not playing!')
        # if a song is selected and the selected song is same as the
        # song playing then pause the music
        else:
            self._pause_music()

    def _click_next(self):
        """
        Play the song below the song selected
        :return: None
        """
        try:
            # get next song index
            next_song_index = self._song_list.curselection()[0] + 1
            # if current song is the last song
            # then the next song is the first song
            if next_song_index == self._song_list.size():
                next_song_index = 0
            # play next song
            self._play_music_by_index(next_song_index)
        except IndexError:
            messagebox.showerror('show error', 'No song selected!')

    def _click_prev(self):
        """
        Play the song above the song selected
        :return: None
        """
        try:
            # get prev song index
            prev_song_index = self._song_list.curselection()[0] - 1
            # if current song is the first song
            # then previous song is the last song
            if prev_song_index == -1:
                prev_song_index = self._song_list.size() - 1
            # play previous song
            self._play_music_by_index(prev_song_index)
        except IndexError:
            messagebox.showerror('show error', 'No song selected!')

    def _click_delete(self):
        """
        Delete the selected music from the Listbox
        :return: None
        """
        try:
            # if the song playing is same as the song to be deleted
            # then pause the song before deleting it and update paused to True
            if self._current_song == self._song_list.get(tk.ACTIVE) and \
                    self._paused is False:
                self._pause_music()
            self._song_list.delete(self._song_list.curselection()[0])
        except IndexError:
            messagebox.showerror('show error', 'No song selected!')

    def _play_music(self):
        """
        Play the current music
        :return: None
        """
        # get current song name
        self._current_song = self._song_list.get(tk.ACTIVE)
        # load current song
        pygame.mixer.music.load(SONGS_DIR / self._current_song)
        # play current song
        pygame.mixer.music.play()
        # update paused status to False
        self._paused = False

    def _pause_music(self):
        """
        pause the music that was playing
        :return:
        """
        # pause the song
        pygame.mixer.music.pause()
        # update paused status to True
        self._paused = True

    def _unpause_music(self):
        """
        unpause the song that was paused
        :return:
        """
        # unpause the song
        pygame.mixer.music.unpause()
        # update paused status to False
        self._paused = False

    def _play_music_by_index(self, song_index):
        """
        activate the selected music
        :return:
        """
        # clear song_list
        self._song_list.selection_clear(0, tk.END)
        # activate next song
        self._song_list.activate(song_index)
        # select next song
        self._song_list.selection_set(song_index)
        # play the music
        self._play_music()


def main():
    # create root window
    root = tk.Tk()
    root.title('Music Player')
    root.resizable(False, False)
    # main app
    MainApp(root)
    # root mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
