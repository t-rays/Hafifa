# Python Clean Code Exercise
Now when you know how to write a basic code in python and know the syntax, we'll see how to write a good code:)

You have a file of a mp3 player that works, but is badly written.

Your mission is to take the code and organize it as much as you can.
To help you, you have a git repo that sums up the principles of Python Clean Code.

You should choose both linter and formater of your choise, run it on the code and present it in the CR.

Good luck!

## Player (`player.py`)

**Run** (from repo root, with venv activated):

```bash
python clean_code/player.py
```

**Dependencies:** `pygame`, `mutagen`

| File | Role |
|------|------|
| `player.py` | Application entry point (`main`) |
| `constants.py` | Shared UI styles, timing, and dialog settings |
| `track.py` | `Track` — immutable song metadata |
| `playlist.py` | `Playlist` — order, index, wrap on next/previous |
| `music_player.py` | `MusicPlayer` — Tk UI and pygame actions |
| `logging_config.py` | Console logging format and startup configuration |

Warnings and errors (bad tags, failed playback, empty playlist) are logged to the terminal as well as shown in the UI where applicable.

**Usage:** ADD TO LIST → pick MP3s → PLAY SONG. Pause and next/previous use the current playlist index.
