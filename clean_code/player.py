import os
from collections.abc import Iterable
from dataclasses import dataclass

import pygame
from mutagen import File, MutagenError
from tkinter import END, WORD, Button, Frame, Label, Text, Tk
from tkinter.filedialog import askopenfilenames

UNKNOWN_ARTIST = "Unknown artist"
SONG_END = pygame.USEREVENT + 1
POLL_INTERVAL_MS = 200

global playlist
global pausing
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


class Playlist:
    def __init__(self) -> None:
        self.tracks: list[Track] = []
        self.index = 0

    @property
    def current(self) -> Track | None:
        if not self.tracks:
            return None
        return self.tracks[self.index]

    def add(self, tracks: Iterable[Track]) -> None:
        self.tracks.extend(tracks)

    def advance(self) -> None:
        if self.tracks:
            self.index = (self.index + 1) % len(self.tracks)

    def rewind(self) -> None:
        if self.tracks:
            self.index = (self.index - 1) % len(self.tracks)


class FrameApp(Frame):
    def __init__(self, master):
        super().__init__(master)
        global text1, label1, playlist, pausing
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
        playlist = Playlist()
        pausing = False


def button1():
    global playlist, text1
    paths = askopenfilenames()
    if not paths:
        return
    playlist.add(Track.from_path(path) for path in paths)
    text1.delete(0.0, END)
    for number, track in enumerate(playlist.tracks, start=1):
        text1.insert(END, f"{number} : {track.label}\n")


def button2():
    global playlist, pausing, label1, SONG_END
    track = playlist.current
    if track is None:
        return
    pygame.mixer.music.load(track.path)
    pygame.mixer.music.play(1, 0.0)
    pygame.mixer.music.set_endevent(SONG_END)
    pausing = False
    label1["text"] = f"Now playing: Nr:{playlist.index + 1} {track.label}"


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


def button5():
    global playlist
    playlist.advance()
    button2()


def button4():
    global playlist
    playlist.rewind()
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
