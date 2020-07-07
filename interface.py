import tkinter
import api_logic
import ffmpeg_script

import typing
from typing import List, Tuple, Iterable
from functools import partial

global search_type

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width = 485, height = 300, )
canvas.place(x = 5, y= 135)

search_type = tkinter.IntVar()
search_type.set(1)

def init_screen() -> None:
    """Creates the general screen of app"""

    root.title("Youtube Video Downloader")

    root.geometry("500x500+650+250")
    root.minsize(width = 500, height = 500)
    root.maxsize(width = 500, height = 500)
    #Setting main screen size, relative initial position, background colour

    tkinter.Label(root, text = "Youtube API Key").place(x= 5, y = 10)
    tkinter.Label(root, text = "Download Location").place(x = 5, y = 50)

    tkinter.Entry(root, name = "api_input", width = 35).place(x = 130, y = 10)
    tkinter.Entry(root, name = "path", width = 35).place(x= 130, y = 50)
    #Creating necessary entry input fields


#Different search mode fellas
def mode_buttons() -> None:
    """Creates the Radiobuttons which control search types"""
    global search_type

    modes = [
        ("Video", 1),
        ("Playlist", 2),
        ("Search", 3),
      ]

    for val, (button_name, button_ID)  in enumerate(modes):
        x_pos = 10 + (100*(val))
        tkinter.Radiobutton(root, text = button_name, padx = 1, pady = 5, indicatoron = 0, 
                            variable = search_type, width = 10, value = button_ID, 
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
    """Changes canvas to video search mode"""
    canvas.delete("all")
    canvas["background"] = "#A9EDFF"
    

def playlist_search_screen():
    """Changes canvas to playlist search mode"""
    canvas.delete("all")
    canvas["background"] = "#09ff00"
    

def youtube_search_screen():
    """Changes canvas to general youtube search mode"""
    canvas.delete("all")
    canvas["background"] = "#ff0000"
    


#Download button and his homie functions
def download_button():
    tkinter.Button(root, text = "DOWNLOAD", name = "download", width = 50, height = 2, 
                    command = partial(download, key = retrieve_key, path = retrieve_path, video = retrieve_video)).place(x = 25, y = 450)

def download(key: str, path: str, video: str) -> None:
    print("download complete :)")
    print(key, path, video)

def retrieve_key() -> str:
    """Retrieves the input from API Input entry field"""
    return find_widgets_by_name("api_input").get()

def retrieve_path() -> str:
    """Retrieves the input from download path entry field"""
    return find_widgets_by_name("path").get()

def retrieve_video():
    pass

def find_widgets_by_name(name: str):
    return root.children[name]




#Experiment bois
def test_button():
    def print_widget(name: str):
        print(find_widgets_by_name(name).get())

    tkinter.Button(root, text = "test", command = partial(print_widget, name = "api_input")).place(x= 400, y = 100)


def enumyrate(iterable: Iterable):
    counter = 0
    for x in iterable:
        yield counter, x
        counter +=1


#The main man :DD
def main():
    init_screen()

    test_button()
    mode_buttons()
    show_mode()
    download_button()

    root.mainloop()

if __name__ == "__main__":
    main()