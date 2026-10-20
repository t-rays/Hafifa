"""Entry point for the MP3 player application.

Run: ``python clean_code/player.py`` (requires pygame, mutagen).

Modules:
  constants     — timing, UI styles, file dialog filters
  track         — ``Track`` metadata model
  playlist      — ``Playlist`` navigation
  music_player  — ``MusicPlayer`` Tk window and pygame actions
  logging_config — console logging setup
"""

import logging

import pygame

from constants import SONG_ENDED
from logging_config import configure_logging
from music_player import MusicPlayer

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the player: logging, Tk window, pygame mixer, then event loop.

    Pygame is initialized after ``MusicPlayer`` so Tk owns the GUI on macOS.
    ``SONG_ENDED`` is registered so ``MusicPlayer`` can auto-advance tracks.
    """
    configure_logging()
    logger.info("Starting MP3 player")
    app = MusicPlayer()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(SONG_ENDED)
    app.mainloop()


if __name__ == "__main__":
    main()
