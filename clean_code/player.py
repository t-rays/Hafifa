import os
from dataclasses import dataclass

import pygame
from mutagen import File, MutagenError
from tkinter import END, WORD, Button, Frame, Label, Text, Tk
from tkinter.filedialog import askopenfilenames

UNKNOWN_ARTIST = "Unknown artist"
SONG_END = pygame.USEREVENT + 1
POLL_INTERVAL_MS = 200

global playlist_tracks
global pausing
global list_index
global text1
global label1


@dataclass(frozen=True)
class Track:
    path: str
    title: str
    artist: str

    @classmethod
    def from_path(cls, path: str) -> "Track":
        filename = os.path.basename(path)
        try:
            tagged = File(path, easy=True)
        except MutagenError:
            tagged = None
        if tagged is None:
            return cls(path, filename, UNKNOWN_ARTIST)
        title = (tagged.get("title") or [filename])[0]
        artist = (tagged.get("artist") or [UNKNOWN_ARTIST])[0]
        return cls(path, str(title), str(artist))

    @property
    def label(self) -> str:
        return f"{self.title} - {self.artist}"


class FrameApp(Frame):
    def __init__(self, master):
        super().__init__(master)
        global text1, label1, playlist_tracks, pausing, list_index
        self.grid()
        Button(self, text="ADD TO LIST", command=button1, bg="AntiqueWhite1", width=40).grid(
            row=1, column=0
        )
        Button(self, text="PLAY SONG", command=button2, bg="AntiqueWhite1", width=40).grid(
            row=2, column=0
        )
        Button(self, text="PAUSE/UNPAUSE", command=button3, bg="AntiqueWhite1", width=40).grid(
            row=3, column=0
        )
        Button(self, text="PREVIOUS SONG", command=button4, bg="AntiqueWhite1", width=40).grid(
            row=4, column=0
        )
        Button(self, text="NEXT SONG", command=button5, bg="AntiqueWhite1", width=40).grid(
            row=5, column=0
        )
        label1 = Label(self, fg="Black", font=("Helvetica 12 bold italic", 10), bg="ivory2")
        label1.grid(row=6, column=0)
        text1 = Text(self, wrap=WORD, width=60)
        text1.grid(row=8, column=0)
        playlist_tracks = []
        pausing = False
        list_index = 0


def button1():
    global list_index, playlist_tracks, pausing, label1, text1
    paths = askopenfilenames()
    if not paths:
        return
    for path in paths:
        playlist_tracks.append(Track.from_path(path))
    text1.delete(0.0, END)
    for key, track in enumerate(playlist_tracks):
        text1.insert(END, f"{key + 1} : {track.label}\n")


def song_data():
    track = playlist_tracks[list_index]
    return f"Now playing: Nr:{list_index + 1} {track.label}"


def button2():
    global list_index, playlist_tracks, pausing, label1, text1
    track = playlist_tracks[list_index]
    pygame.mixer.music.load(track.path)
    pygame.mixer.music.play(1, 0.0)
    pygame.mixer.music.set_endevent(SONG_END)
    pausing = False
    label1["text"] = song_data()


def check_music():
    for event in pygame.event.get():
        if event.type == SONG_END:
            button5()


def button3():
    global pausing
    if pausing:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    pausing = not pausing


def get_next_song():
    if list_index + 2 <= len(playlist_tracks):
        return list_index + 1
    return 0


def button5():
    global list_index
    list_index = get_next_song()
    button2()


def get_previous_song():
    if list_index - 1 >= 0:
        return list_index - 1
    return len(playlist_tracks) - 1


def button4():
    global list_index
    list_index = get_previous_song()
    button2()


def main() -> None:
    window = Tk()
    window.geometry("500x500")
    window.title("MP3 Music Player")
    pygame.init()
    app = FrameApp(window)

    def poll_song_end() -> None:
        check_music()
        app.after(POLL_INTERVAL_MS, poll_song_end)

    poll_song_end()
    app.mainloop()


if __name__ == "__main__":
    main()
