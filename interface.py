import tkinter
import api_logic
import ffmpeg_script

import typing
from typing import List, Tuple

#My guy what is my plan for the design here

root = tkinter.Tk()

def init_screen()  -> None:
    """Creates the general screen of app"""

    root.title("Youtube Video Downloader")
    #Making Main Screen

    root.geometry("500x500+650+250")
    root.minsize(width = 500, height = 500)
    root.maxsize(width = 500, height = 500)
    root["background"] = "#c4c2ff"

    #Setting main screen size, relative initial position, background colour

if __name__ == "__main__":
    init_screen()

    root.mainloop()