from tkinter import *
import pygame
import os
from tkinter import messagebox

SONGS_PATH = os.getcwd() + '/audio'
IMAGE_PATH = os.getcwd() + '/logo'


def get_images():
    img_names = ['play', 'pause', 'next', 'prev', 'trash']
    img_dict = {}
    for name in img_names:
        img_dict[name] = PhotoImage(file=f'{IMAGE_PATH}/{name}.png')
    return img_dict


class MainApp:
    def __init__(self, parent):
        self.parent = parent
        self.song_list = Listbox(self.parent, bg='black', fg='white',
                                 height=25,
                                 width=55)
        self.song_list.grid(row=0, column=0)

        self.buttons_frame = Frame(self.parent)
        self.buttons_frame.grid(row=1, column=0)

        self.images = get_images()
        self.current_song = None
        self.paused = False

        # create buttons
        button_dict = {
            'prev': [1, self.click_prev],
            'play': [2, self.click_play],
            'pause': [3, self.click_pause],
            'next': [4, self.click_next],
            'trash': [5, self.click_delete]
        }
        for k, v in button_dict.items():
            Button(self.buttons_frame, image=self.images[k], command=v[1]) \
                .grid(row=0, column=v[0], padx=10, pady=10)

        # display the songs in the specified folder
        self.display_music()

    def click_play(self):
        """
        check whether to play the music or not
        :return: None
        """
        # check if a song is selected
        if self.song_list.curselection() == ():
            messagebox.showerror('show error', 'no song selected!')
        # if the song paused is same as the song selected
        # then unpause the song and update paused to False
        elif self.current_song == self.song_list.get(ACTIVE) and self.paused:
            self.unpause_music()
        # otherwise, just play the song selected
        # and update the current song to the song selected
        else:
            self.play_music()

    def click_pause(self):
        """
        check whether to pause the music or not
        :return: None
        """
        # if no song is selected
        if self.song_list.curselection() == ():
            messagebox.showerror('show error', 'no song selected!')
        # if no song is playing
        elif self.paused is True:
            messagebox.showerror('show error', 'no song is playing')
        # if a song is selected but the selected song is different from the
        # song playing
        elif self.current_song != self.song_list.get(ACTIVE):
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
            messagebox.showerror('show error', 'No song selected!')

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
            messagebox.showerror('show error', 'No song selected!')

    def click_delete(self):
        """
        Delete the selected music from the Listbox
        :return: None
        """
        try:
            # if the song playing is same as the song to be deleted
            # then pause the song before deleting it and update paused to True
            if self.current_song == self.song_list.get(ACTIVE) and \
                    self.paused is False:
                self.pause_music()
            self.song_list.delete(self.song_list.curselection()[0])
        except IndexError:
            messagebox.showerror('show error', 'No song selected!')

    def play_music(self):
        """
        Play the current music
        :return: None
        """
        # get current song name
        self.current_song = self.song_list.get(ACTIVE)
        # load current song
        pygame.mixer.music.load(os.path.join(
            SONGS_PATH, self.current_song))
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
        self.song_list.selection_clear(0, END)
        # activate next song
        self.song_list.activate(song_index)
        # select next song
        self.song_list.selection_set(song_index)
        # play the music
        self.play_music()

    def display_music(self):
        """
        Display songs in SONG_PATH onto song_list
        :return: None
        """
        # display songs to the song_list
        for song in os.listdir(SONGS_PATH):
            if song.endswith(".mp3"):
                self.song_list.insert(END, song)
        # clear song box
        self.song_list.selection_clear(0, END)
        # activate first song
        self.song_list.activate(0)
        # select first song
        self.song_list.selection_set(0)


def main():
    # create root window
    root = Tk()
    root.title('Music Player')
    root.resizable(False, False)
    # initialize mixer
    pygame.mixer.init()
    # main app
    MainApp(root)
    # root mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
