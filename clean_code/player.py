"""Entry point for the MP3 player application.

Run: ``python clean_code/player.py`` (requires pygame, mutagen).

Modules:
  constants     — timing, UI styles, file dialog filters
  track         — ``Track`` metadata model
  playlist      — ``Playlist`` navigation
  music_player  — ``MusicPlayer`` Tk window and pygame actions
"""

import pygame

from constants import SONG_ENDED
from music_player import MusicPlayer


def main() -> None:
    """Create the Tk window first, then init pygame (macOS-friendly order)."""
    app = MusicPlayer()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(SONG_ENDED)
    app.mainloop()


if __name__ == "__main__":
    main()
