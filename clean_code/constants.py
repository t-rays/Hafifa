"""Shared configuration and UI defaults for the MP3 player."""

import pygame
from tkinter import WORD

POLL_INTERVAL_MS = 200
UNKNOWN_ARTIST = "Unknown artist"
SONG_ENDED = pygame.USEREVENT + 1

WINDOW_TITLE = "MP3 Music Player"
WINDOW_GEOMETRY = "500x500"

BUTTON_STYLE = {"bg": "AntiqueWhite1", "width": 40}
NOW_PLAYING_STYLE = {
    "fg": "Black",
    "bg": "ivory2",
    "font": ("Helvetica", 10, "bold italic"),
}
PLAYLIST_STYLE = {"wrap": WORD, "width": 60, "height": 12}

MP3_FILE_TYPES = [("MP3 files", "*.mp3")]
