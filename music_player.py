import tkinter as tk
from tkinter import messagebox, filedialog
import pygame
from pathlib import Path
from typing import Dict

SONGS_DIR = Path('audio')
IMAGE_DIR = Path('logo')

BUTTONS = {
    'add': [1, 'click_add'],
    'prev': [2, 'click_prev'],
    'play': [3, 'click_play'],
    'pause': [4, 'click_pause'],
    'next': [5, 'click_next'],
    'trash': [6, 'click_delete'],
}


class MainApp:
    def __init__(self, root):
        self.root = root
        self.image_dict = self.load_images()
        self.current_song = None
        self.paused = False
        self._init_ui()
        self._init_sound()

    def _init_ui(self):
        self.song_list = tk.Listbox(self.root,
                                    bg='black', fg='white', height=25,
                                    width=55)
        self.song_list.grid(row=0, column=0)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=1, column=0)

        for name, (row, callback) in BUTTONS.items():
            button = tk.Button(self.buttons_frame, image=self.image_dict[name],
                               command=getattr(self, callback))
            button.grid(row=0, column=row, padx=10, pady=10)

    def _init_sound(self):
        pygame.init()

    def load_images(self) -> Dict[str, tk.PhotoImage]:
        img_names = ['add', 'play', 'pause', 'next', 'prev', 'trash']
        return {
            name: tk.PhotoImage(file=IMAGE_DIR / f'{name}.png')
            for name in img_names
        }

    def click_add(self):
        # add songs to the song_list
        song = filedialog.askopenfilename(initialdir=SONGS_DIR,
                                          title='Choose a song')
        self.song_list.insert(tk.END, song[song.rfind('/') + 1:])

    def click_play(self):
        # check if a song is selected
        if self.song_list.curselection() == ():
            messagebox.showerror('show error', 'no song selected!')
        # if the song paused is same as the song selected
        # then unpause the song and update paused to False
        elif self.current_song == self.song_list.get(
                tk.ACTIVE) and self.paused:
            self.unpause_music()
        # otherwise, just play the song selected
        # and update the current song to the song selected
        else:
            self.play_music()

    def click_pause(self):
        # if no song is selected
        if self.song_list.curselection() == ():
            messagebox.showerror('show error', 'no song selected!')
        # if no song is playing
        elif self.paused is True:
            messagebox.showerror('show error', 'no song is playing!')
        # if a song is selected but the selected song is different from the
        # song playing
        elif self.current_song != self.song_list.get(tk.ACTIVE):
            messagebox.showerror('show error',
                                 'the selected song is not playing!')
        # if a song is selected and the selected song is same as the
        # song playing then pause the music
        else:
            self.pause_music()

    def click_next(self):
        """
        Play the song below the song selected
        :return: None
        """
        try:
            # get next song index
            next_song_index = self.song_list.curselection()[0] + 1
            # if current song is the last song
            # then the next song is the first song
            if next_song_index == self.song_list.size():
                next_song_index = 0
            # play next song
            self.play_music_by_index(next_song_index)
        except IndexError:
            messagebox.showerror('show error', 'no song selected!')

    def click_prev(self):
        """
        Play the song above the song selected
        :return: None
        """
        try:
            # get prev song index
            prev_song_index = self.song_list.curselection()[0] - 1
            # if current song is the first song
            # then previous song is the last song
            if prev_song_index == -1:
                prev_song_index = self.song_list.size() - 1
            # play previous song
            self.play_music_by_index(prev_song_index)
        except IndexError:
            messagebox.showerror('show error', 'no song selected!')

    def click_delete(self):
        """
        Delete the selected music from the Listbox
        :return: None
        """
        try:
            # if the song playing is same as the song to be deleted
            # then pause the song before deleting it and update paused to True
            if self.current_song == self.song_list.get(tk.ACTIVE) and \
                    self.paused is False:
                self.pause_music()
            self.song_list.delete(self.song_list.curselection()[0])
        except IndexError:
            messagebox.showerror('show error', 'no song selected!')

    def play_music(self):
        """
        Play the current music
        :return: None
        """
        # get current song name
        self.current_song = self.song_list.get(tk.ACTIVE)
        # load current song
        pygame.mixer.music.load(SONGS_DIR / self.current_song)
        # play current song
        pygame.mixer.music.play()
        # update paused status to False
        self.paused = False

    def pause_music(self):
        """
        pause the music that was playing
        :return:
        """
        # pause the song
        pygame.mixer.music.pause()
        # update paused status to True
        self.paused = True

    def unpause_music(self):
        """
        unpause the song that was paused
        :return:
        """
        # unpause the song
        pygame.mixer.music.unpause()
        # update paused status to False
        self.paused = False

    def play_music_by_index(self, song_index):
        """
        activate the selected music
        :return:
        """
        # clear song_list
        self.song_list.selection_clear(0, tk.END)
        # activate next song
        self.song_list.activate(song_index)
        # select next song
        self.song_list.selection_set(song_index)
        # play the music
        self.play_music()


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
