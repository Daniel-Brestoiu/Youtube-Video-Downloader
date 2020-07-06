import tkinter
import api_logic
import ffmpeg_script

import typing
from typing import List, Tuple

global search_type

root = tkinter.Tk()

search_type = tkinter.IntVar()

def init_screen() -> None:
    """Creates the general screen of app"""

    root.title("Youtube Video Downloader")

    root.geometry("500x500+650+250")
    root.minsize(width = 500, height = 500)
    root.maxsize(width = 500, height = 500)
    #Setting main screen size, relative initial position, background colour

    tkinter.Label(root, text = "Youtube API Key").place(x= 5, y = 10)
    tkinter.Label(root, text = "Download Location").place(x = 5, y = 50)

    API_input = tkinter.Entry(root, width = 35).place(x = 130, y = 10)
    download_path = tkinter.Entry(root, width = 35).place(x= 130, y = 50)
    #Creating necessary entry input fields

def mode_buttons() -> None:
    """Creates the Radiobuttons which control search types"""
    global search_type

    modes = [
        ("Video", 1),
        ("Playlist", 2),
        ("Search", 3),
      ]

    for val, mode  in enumerate(modes):
        x_pos = 10 + (100*(int(val)))
        tkinter.Radiobutton(root, text = mode[0], padx = 1, pady = 5, indicatoron = 0, 
                            variable = search_type, width = 10, value = mode[1], 
                            command = lambda: show_mode()).place(x = x_pos, y = 100)

def show_mode() -> None:
    """Interprets which radio button is pressed and calls the function to create its search type"""

    selected_mode = search_type.get()
    # Video = 1, Playlist = 2, Search = 3

    if selected_mode == 1:
        video_search_screen()
    
    elif selected_mode == 2:
        playlist_search_screen()

    elif selected_mode == 3:
        youtube_search_screen()

def video_search_screen():
    pass
def playlist_search_screen():
    pass
def youtube_search_screen():
    pass


    



if __name__ == "__main__":
    init_screen()

    mode_buttons()

    root.mainloop()