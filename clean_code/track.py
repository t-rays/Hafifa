"""Track metadata model."""

import os
from dataclasses import dataclass

from mutagen import File, MutagenError

from constants import UNKNOWN_ARTIST


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
