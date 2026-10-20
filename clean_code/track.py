"""Track metadata model."""

import logging
import os
from dataclasses import dataclass

from mutagen import File, MutagenError

from constants import TAG_VALUE_INDEX, UNKNOWN_ARTIST

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Track:
    """One audio file and its display metadata."""

    path: str
    title: str
    artist: str

    @classmethod
    def from_path(cls, path: str) -> "Track":
        """Build a track from a file path, reading ID3 tags a single time.

        Args:
            path: Absolute or relative path to an audio file on disk.

        Returns:
            A ``Track`` with title/artist from tags, or filename / unknown artist
            when tags are missing or unreadable.
        """
        filename = os.path.basename(path)
        try:
            tagged = File(path, easy=True)
        except MutagenError as error:
            logger.warning("Could not read tags for %s: %s", path, error)
            tagged = None
        if tagged is None:
            logger.debug("Using filename fallback for %s", path)
            return cls(path, filename, UNKNOWN_ARTIST)
        title = (tagged.get("title") or [filename])[TAG_VALUE_INDEX]
        artist = (tagged.get("artist") or [UNKNOWN_ARTIST])[TAG_VALUE_INDEX]
        return cls(path, str(title), str(artist))

    @property
    def label(self) -> str:
        """Human-readable ``title - artist`` string for UI and logs."""
        return f"{self.title} - {self.artist}"
