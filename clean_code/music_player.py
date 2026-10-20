"""Tkinter UI and pygame playback.

``MusicPlayer`` binds user actions to ``Playlist`` state and the pygame mixer.
End-of-track handling uses Tk's ``after`` scheduler rather than a busy loop.
"""

import logging

import pygame
from tkinter import END, Button, Label, Text, Tk
from tkinter.filedialog import askopenfilenames

from constants import (
    BUTTON_STYLE,
    FIRST_TRACK_NUMBER,
    MP3_FILE_TYPES,
    NOW_PLAYING_STYLE,
    PLAYLIST_STYLE,
    PLAYLIST_TEXT_START,
    POLL_INTERVAL_MS,
    SONG_ENDED,
    WINDOW_GEOMETRY,
    WINDOW_RESIZABLE,
    WINDOW_TITLE,
)
from playlist import Playlist
from track import Track

logger = logging.getLogger(__name__)


class MusicPlayer(Tk):
    """Main window: file picker, controls, playlist view, and mixer actions."""

    def __init__(self) -> None:
        """Lay out controls and start periodic checks for track end events."""
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_GEOMETRY)
        self.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)

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
        """Open a file dialog, append chosen MP3s, and refresh the playlist view.

        Each path is turned into a ``Track`` (tags read once). Does nothing if
        the user cancels the dialog.
        """
        paths = askopenfilenames(filetypes=MP3_FILE_TYPES)
        if not paths:
            return
        self.playlist.add(Track.from_path(path) for path in paths)
        logger.info("Added %d track(s) to the playlist", len(paths))
        self._show_playlist()

    def play_current(self) -> None:
        """Load and play the track at the playlist's current index.

        Updates the now-playing label on success. On failure, logs a warning
        and shows a short error message without changing the playlist index.
        """
        track = self.playlist.current
        if track is None:
            logger.warning("Play requested but the playlist is empty")
            return
        try:
            pygame.mixer.music.load(track.path)
        except pygame.error as error:
            logger.warning("Cannot play %s: %s", track.path, error)
            self.now_playing["text"] = f"Cannot play: {track.title}"
            return
        pygame.mixer.music.play()
        self.paused = False
        track_number = self.playlist.index + FIRST_TRACK_NUMBER
        self.now_playing["text"] = f"Now playing: Nr:{track_number} {track.label}"

    def toggle_pause(self) -> None:
        """Pause or resume the current mixer stream, if one is active."""
        try:
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        except pygame.error as error:
            logger.warning("Pause toggle failed: %s", error)
            return
        self.paused = not self.paused

    def play_next(self) -> None:
        """Move to the next track (wrapping) and start playback."""
        self.playlist.advance()
        self.play_current()

    def play_previous(self) -> None:
        """Move to the previous track (wrapping) and start playback."""
        self.playlist.rewind()
        self.play_current()

    def _show_playlist(self) -> None:
        """Rewrite the text widget from the in-memory playlist (1-based lines)."""
        self.playlist_view.delete(PLAYLIST_TEXT_START, END)
        for number, track in enumerate(
            self.playlist.tracks, start=FIRST_TRACK_NUMBER
        ):
            self.playlist_view.insert(END, f"{number} : {track.label}\n")

    def _poll_song_end(self) -> None:
        """Check pygame for end-of-song events and schedule the next poll."""
        if any(event.type == SONG_ENDED for event in pygame.event.get()):
            self.play_next()
        self.after(POLL_INTERVAL_MS, self._poll_song_end)
