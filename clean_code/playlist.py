"""Playlist state and navigation."""

from collections.abc import Iterable

from track import Track


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
