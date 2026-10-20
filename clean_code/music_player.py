"""Tkinter UI and pygame playback."""

import pygame
from tkinter import END, Button, Label, Text, Tk
from tkinter.filedialog import askopenfilenames

from constants import (
    BUTTON_STYLE,
    MP3_FILE_TYPES,
    NOW_PLAYING_STYLE,
    PLAYLIST_STYLE,
    POLL_INTERVAL_MS,
    SONG_ENDED,
    WINDOW_GEOMETRY,
    WINDOW_TITLE,
)
from playlist import Playlist
from track import Track


class MusicPlayer(Tk):
    """Main window: file picker, controls, playlist view, and mixer actions."""

    def __init__(self) -> None:
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_GEOMETRY)
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
