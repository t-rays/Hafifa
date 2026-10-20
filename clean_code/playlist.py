"""Playlist state and navigation.

``Playlist`` holds track order and a single cursor (``index``). Navigation
methods wrap at both ends so next/previous always stay in range.
"""

from collections.abc import Iterable

from constants import (
    INITIAL_PLAYLIST_INDEX,
    PLAYLIST_STEP_BACKWARD,
    PLAYLIST_STEP_FORWARD,
)
from track import Track


class Playlist:
    """Ordered tracks with a current position that wraps at both ends."""

    def __init__(self) -> None:
        self.tracks: list[Track] = []
        self.index = INITIAL_PLAYLIST_INDEX

    @property
    def current(self) -> Track | None:
        """The track at ``index``, or ``None`` when the playlist is empty."""
        if not self.tracks:
            return None
        return self.tracks[self.index]

    def add(self, tracks: Iterable[Track]) -> None:
        """Append tracks to the end of the playlist without changing ``index``."""
        self.tracks.extend(tracks)

    def advance(self) -> None:
        """Select the next track; wraps from last to first."""
        self._move(PLAYLIST_STEP_FORWARD)

    def rewind(self) -> None:
        """Select the previous track; wraps from first to last."""
        self._move(PLAYLIST_STEP_BACKWARD)

    def _move(self, offset: int) -> None:
        """Shift ``index`` by ``offset`` with modulo wrap when non-empty."""
        if self.tracks:
            self.index = (self.index + offset) % len(self.tracks)
