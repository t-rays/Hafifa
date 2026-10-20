from mutagen.easyid3 import EasyID3
import pygame
from tkinter import END, WORD, Button, Frame, Label, Text, Tk
from tkinter.filedialog import askopenfilenames

global list1
global pausing
global list_index
global SONG_END
global text1
global label1


class FrameApp(Frame):
    def __init__(self, master):
        super(FrameApp, self).__init__(master)
        global text1, label1, list1, pausing, list_index, SONG_END
        self.grid()
        b1 = Button(self, text="PLAY SONG", command=button2, bg="AntiqueWhite1", width=40)
        b1.grid(row=2, column=0)
        b2 = Button(self, text="PREVIOUS SONG", command=button4, bg="AntiqueWhite1", width=40)
        b2.grid(row=4, column=0)
        b3 = Button(self, text="PAUSE/UNPAUSE", command=button3, bg="AntiqueWhite1", width=40)
        b3.grid(row=3, column=0)
        b4 = Button(self, text="NEXT SONG", command=button5, bg="AntiqueWhite1", width=40)
        b4.grid(row=5, column=0)
        b5 = Button(self, text="ADD TO LIST", command=button1, bg="AntiqueWhite1", width=40)
        b5.grid(row=1, column=0)
        label1 = Label(self, fg="Black", font=("Helvetica 12 bold italic", 10), bg="ivory2")
        label1.grid(row=6, column=0)
        text1 = Text(self, wrap=WORD, width=60)
        text1.grid(row=8, column=0)
        list1 = list()
        pausing = False
        list_index = 0
        SONG_END = pygame.USEREVENT + 1


def button1():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        directory = askopenfilenames()
        for song_dir in directory:
            list1.append(song_dir)
        text1.delete(0.0, END)

        for key, item in enumerate(list1):
            song = EasyID3(item)
            song_data = (
                str(key + 1) + " : " + song["title"][0] + " - " + song["artist"][0]
            )
            text1.insert(END, song_data + "\n")
    except Exception:
        pass


def song_data():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        song = EasyID3(list1[list_index])
        return (
            "Now playing: Nr:"
            + str(list_index + 1)
            + " "
            + str(song["title"])
            + " - "
            + str(song["artist"])
        )
    except Exception:
        pass


def button2():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        directory = list1[list_index]
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_endevent(SONG_END)
        pausing = False
        label1["text"] = song_data()
    except Exception:
        pass


def check_music():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        for event in pygame.event.get():
            if event.type == SONG_END:
                button5()
    except Exception:
        pass


def button3():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        if pausing:
            pygame.mixer.music.unpause()
            pausing = False
        elif not pausing:
            pygame.mixer.music.pause()
            pausing = True
    except Exception:
        pass


def get_next_song():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        if list_index + 2 <= len(list1):
            return list_index + 1
        return 0
    except Exception:
        pass


def button5():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        list_index = get_next_song()
        button2()
    except Exception:
        pass


def get_previous_song():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        if list_index - 1 >= 0:
            return list_index - 1
        return len(list1) - 1
    except Exception:
        pass


def button4():
    global list_index, list1, SONG_END, pausing, label1, text1
    try:
        list_index = get_previous_song()
        button2()
    except Exception:
        pass


POLL_INTERVAL_MS = 200


def main() -> None:
    window = Tk()
    window.geometry("500x500")
    window.title("MP3 Music Player")
    pygame.init()
    app = FrameApp(window)

    def poll_song_end() -> None:
        check_music()
        app.after(POLL_INTERVAL_MS, poll_song_end)

    poll_song_end()
    app.mainloop()


if __name__ == "__main__":
    main()
