"""Tkinter MP3 player: Track metadata, Playlist navigation, pygame playback.

Run: ``python clean_code/player.py`` (requires pygame, mutagen).

Layers:
  Track     — path + title/artist (tags read once in ``from_path``)
  Playlist  — ordered list, current index, wrap on next/previous
  MusicPlayer — UI and pygame; polls for end-of-track via ``after()``
"""
import os
from collections.abc import Iterable
from dataclasses import dataclass

import pygame
from mutagen import File, MutagenError
from tkinter import END, WORD, Button, Label, Text, Tk
from tkinter.filedialog import askopenfilenames

SONG_ENDED = pygame.USEREVENT + 1
POLL_INTERVAL_MS = 200
UNKNOWN_ARTIST = "Unknown artist"

BUTTON_STYLE = {"bg": "AntiqueWhite1", "width": 40}
NOW_PLAYING_STYLE = {
    "fg": "Black",
    "bg": "ivory2",
    "font": ("Helvetica", 10, "bold italic"),
}
PLAYLIST_STYLE = {"wrap": WORD, "width": 60, "height": 12}

MP3_FILE_TYPES = [("MP3 files", "*.mp3")]


@dataclass(frozen=True)
class Track:
    """One audio file and its display metadata."""

    path: str
    title: str
    artist: str

    @classmethod
    def from_path(cls, path: str) -> "Track":
        """Read tags once; fall back to the filename if they are missing."""
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
    """Ordered tracks with a current position that wraps at both ends."""

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
        self._move(+1)

    def rewind(self) -> None:
        self._move(-1)

    def _move(self, offset: int) -> None:
        if self.tracks:
            self.index = (self.index + offset) % len(self.tracks)


class MusicPlayer(Tk):
    """Main window: file picker, controls, playlist view, and mixer actions."""

    def __init__(self) -> None:
        super().__init__()
        self.title("MP3 Music Player")
        self.geometry("500x500")
        self.resizable(False, False)

        self.playlist = Playlist()
        self.paused = False

        self._build_widgets()
        self.after(POLL_INTERVAL_MS, self._poll_song_end)

    def _build_widgets(self) -> None:
        controls = (
            ("ADD TO LIST", self.add_songs),
            ("PLAY SONG", self.play_current),
            ("PAUSE/UNPAUSE", self.toggle_pause),
            ("PREVIOUS SONG", self.play_previous),
            ("NEXT SONG", self.play_next),
        )
        for label, command in controls:
            Button(self, text=label, command=command, **BUTTON_STYLE).pack()

        self.now_playing = Label(self, **NOW_PLAYING_STYLE)
        self.now_playing.pack()

        self.playlist_view = Text(self, **PLAYLIST_STYLE)
        self.playlist_view.pack()

    def add_songs(self) -> None:
        paths = askopenfilenames(filetypes=MP3_FILE_TYPES)
        if not paths:
            return
        self.playlist.add(Track.from_path(path) for path in paths)
        self._show_playlist()

    def play_current(self) -> None:
        track = self.playlist.current
        if track is None:
            return
        try:
            pygame.mixer.music.load(track.path)
        except pygame.error:
            self.now_playing["text"] = f"Cannot play: {track.title}"
            return
        pygame.mixer.music.play()
        self.paused = False
        number = self.playlist.index + 1
        self.now_playing["text"] = f"Now playing: Nr:{number} {track.label}"

    def toggle_pause(self) -> None:
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    def play_next(self) -> None:
        self.playlist.advance()
        self.play_current()

    def play_previous(self) -> None:
        self.playlist.rewind()
        self.play_current()

    def _show_playlist(self) -> None:
        self.playlist_view.delete("1.0", END)
        for number, track in enumerate(self.playlist.tracks, start=1):
            self.playlist_view.insert(END, f"{number} : {track.label}\n")

    def _poll_song_end(self) -> None:
        if any(event.type == SONG_ENDED for event in pygame.event.get()):
            self.play_next()
        self.after(POLL_INTERVAL_MS, self._poll_song_end)


def main() -> None:
    """Create the Tk window first, then init pygame (macOS-friendly order)."""
    app = MusicPlayer()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(SONG_ENDED)
    app.mainloop()


if __name__ == "__main__":
    main()
