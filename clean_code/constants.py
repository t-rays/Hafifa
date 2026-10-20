"""Shared configuration and UI defaults for the MP3 player."""

import pygame
from tkinter import WORD

# Playback / events
POLL_INTERVAL_MS = 200
SONG_ENDED = pygame.USEREVENT + 1

# Window
WINDOW_TITLE = "MP3 Music Player"
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
WINDOW_RESIZABLE = False

# Playlist state
INITIAL_PLAYLIST_INDEX = 0
PLAYLIST_STEP_FORWARD = 1
PLAYLIST_STEP_BACKWARD = -1
FIRST_TRACK_NUMBER = 1

# Widget layout
BUTTON_WIDTH = 40
NOW_PLAYING_FONT_SIZE = 10
PLAYLIST_TEXT_WIDTH = 60
PLAYLIST_TEXT_HEIGHT = 12
PLAYLIST_TEXT_START = "1.0"

# Metadata parsing
TAG_VALUE_INDEX = 0

UNKNOWN_ARTIST = "Unknown artist"

BUTTON_STYLE = {"bg": "AntiqueWhite1", "width": BUTTON_WIDTH}
NOW_PLAYING_STYLE = {
    "fg": "Black",
    "bg": "ivory2",
    "font": ("Helvetica", NOW_PLAYING_FONT_SIZE, "bold italic"),
}
PLAYLIST_STYLE = {
    "wrap": WORD,
    "width": PLAYLIST_TEXT_WIDTH,
    "height": PLAYLIST_TEXT_HEIGHT,
}

MP3_FILE_TYPES = [("MP3 files", "*.mp3")]
