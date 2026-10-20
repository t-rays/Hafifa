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

| Component | Role |
|-----------|------|
| `Track` | Immutable song; ID3 read once when adding files |
| `Playlist` | Track list + index; next/previous wrap around |
| `MusicPlayer` | Tk UI, user actions, pygame mixer, end-of-song polling |

**Usage:** ADD TO LIST → pick MP3s → PLAY SONG. Pause and next/previous use the current playlist index.
