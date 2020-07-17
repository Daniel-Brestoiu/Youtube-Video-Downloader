import re
import urllib.request
import tempfile
import tkinter
import ffmpeg_script
import api_logic
import typing

from tkinter import filedialog
from ffmpeg_script import download_videos
from api_logic import search_video
from typing import List, Tuple, Iterable, IO, Any
from functools import partial
from PIL import Image, ImageTk

root = tkinter.Tk()
canvas = tkinter.Canvas(root, name = "canvas", width = 485, height = 300, )
canvas.place(x = 5, y= 135)

THUMBNAILS_LIST = []

SEARCH_TYPE = tkinter.IntVar()
SEARCH_TYPE.set(1)

EYE_CLOSED_IMAGE = tkinter.PhotoImage(file = "password eye closed.png") # Mode 0
EYE_OPEN_IMAGE = tkinter.PhotoImage(file = "password eye open.png") # Mode 1 
EYE_MODE = 0

class Thumbnail_Image():
    def __init__(self, url: str = None, temp_file: IO[Any] = None, scale: int = None, width: int = None, height: int = None, image = None):
        global THUMBNAILS_LIST

        self.url = url
        self.temp_file = temp_file
        self.scale = scale
        self.width = width
        self.height = height
        self.image = image

        THUMBNAILS_LIST.append(self)

    
    def download_from_url(self) -> None:
        """Downloads contents from self.url and stores it in a temp file referenced as self.temp_file."""
        self.temp_file = tempfile.NamedTemporaryFile()
        urllib.request.urlretrieve(url = self.url, filename= self.temp_file.name)
    
    def place_thumbnail_from_temp(self) -> None:
        """Takes image stored in self.temp_file, and stores it in self.image -> places self.image on canvas using tkinter canvas.create_image()"""
        self.image = ImageTk.PhotoImage(Image.open(self.temp_file.name))
        thumbnail_placeholder = canvas.create_image((self.scale/2 + 20, self.scale/2 + 5), image = self.image)
    
    def place_thumbnail_from_image(self) -> None:
        """Places self.image on canvas using tkinter canvas.create_image()."""
        thumbnail_placeholder = canvas.create_image((self.scale/2 + 20, self.scale/2 + 5), image = self.image)

    def destroy(self) -> None:
        """If there is a temp file referenced by self.temp_file, properly closes the temp file."""
        if self.temp_file is not None:
            self.temp_file.close()


def init_screen() -> None:
    """Creates the general screen of app"""

    root.title("Youtube Video Downloader")

    root.geometry("500x500+650+250")
    root.minsize(width = 500, height = 500)
    root.maxsize(width = 500, height = 500)
    #Setting main screen size, relative initial position, background colour

    tkinter.Label(root, text = "Youtube API Key").place(x= 5, y = 10)
    tkinter.Label(root, text = "Download Location").place(x = 5, y = 50)

    tkinter.Entry(root, name = "api_input", width = 39).place(x = 130, y = 10)
    tkinter.Entry(root, name = "path", width = 30).place(x= 130, y = 50)
    
    tkinter.Button(root, name = "path_button", text = "Browse", width = 8, command = select_path).place(x = 415, y = 53)
    tkinter.Button(root, name = "secret_button", image = EYE_CLOSED_IMAGE, command = swap_entry_mode).place(x = 466, y = 12)

def select_path() -> None:
    """Opens popup prompting user to pick a directory. Fills 'path' entry widget with path."""

    root.update()
    directory = str(tkinter.filedialog.askdirectory(title= "Download Path Selection", parent= root))
    root.update()
   
    entry = find_widgets_by_name("path")
    entry.delete(0, "end")
    entry.insert(0, directory)


#Different search mode fellas
def mode_buttons() -> None:
    """Creates the Radiobuttons which control search types"""
    global SEARCH_TYPE

    modes = [
        ("Video", 1),
        ("Playlist", 2),
        ("Search", 3),
      ]

    for val, (button_name, button_ID)  in enumerate(modes):
        x_pos = 10 + (100*(val))
        tkinter.Radiobutton(root, text = button_name, padx = 1, pady = 5, indicatoron = 0, 
                            variable = SEARCH_TYPE, width = 10, value = button_ID, 
                            command = lambda: show_mode()).place(x = x_pos, y = 97)

def show_mode() -> None:
    """Interprets which radio button is pressed and calls the function to create its search type"""

    selected_mode = SEARCH_TYPE.get()
    # Video = 1, Playlist = 2, Search = 3

    if selected_mode == 1:
        video_search_screen()
    elif selected_mode == 2:
        playlist_search_screen()
    elif selected_mode == 3:
        youtube_search_screen()

def video_search_screen():
    """Changes canvas to video search mode"""

    def search() -> None:

        video_id = get_video_id()
        video_link = get_video_link()
        api_key_input = get_api_key()

        title, channel_name, thumbnail_link, thumbnail_width, thumbnail_height = search_video(video_id = video_id, video_link = video_link, API_KEY= api_key_input)

        find_canvas_widget_by_name("video found label")["text"] = title
        find_canvas_widget_by_name("youtuber of video label")["text"] = channel_name
        
        clear_thumbnails()
        thumbnail = Thumbnail_Image(url = thumbnail_link, width = thumbnail_width, height = thumbnail_height, scale = 100)
        thumbnail.download_from_url()
        thumbnail.place_thumbnail_from_temp()

        canvas.update()
        

    def get_video_id() -> str:
        """Returns the text of video id entry field"""
        return find_canvas_widget_by_name("video id").get()

    def get_video_link() -> str:
        """Returns the text of video link entry field"""
        return find_canvas_widget_by_name("video link").get()

    def get_api_key() -> str:
        """Returns the text of the api_input entry field"""
        return find_widgets_by_name("api_input").get()

    clear_canvas()

    canvas["background"] = "#A9EDFF"

    photo = resize_image("placeholder_image.png", 100, 100)
    placeholder_thumbnail = Thumbnail_Image(scale = 100, image = photo)
    placeholder_thumbnail.place_thumbnail_from_image()


    tkinter.Label(canvas, name = "video id label", text = "Video ID:", width = 10, anchor = "w", bg = "#A9EDFF",).place(x = 17, y = 124)
    tkinter.Label(canvas, name = "video link label", text = "Video Link:", width = 10, anchor = "w", bg = "#A9EDFF",).place(x= 17, y = 164) 
    tkinter.Label(canvas, name = "video found label", text = "No Video Searched Yet", bg = "#A9EDFF", anchor = "w",).place(x =145, y = 25)
    tkinter.Label(canvas, name = "youtuber of video label", text = "No Channel Posted This Video", bg = "#A9EDFF", anchor = "w").place(x = 145, y = 55)
    tkinter.Label(canvas, name = "instructions label", text = "Provide input then click search. Download if correct video is found.", bg = "#A9EDFF", anchor = "w").place(x = 20, y = 220)

    tkinter.Entry(canvas, name = "video id", width = 40).place(x = 100, y = 125)
    tkinter.Entry(canvas, name = "video link", width = 40).place(x = 100, y = 165)

    tkinter.Button(canvas, name = "search by video button", text = "SEARCH", width = 50, height = 2, 
                    command = search).place(x= 20, y = 250)

    canvas.update()


def playlist_search_screen() -> None:
    """Changes canvas to playlist search mode"""
    
    clear_canvas()

    canvas["background"] = "#09ff00"    
    canvas.update()
    

def youtube_search_screen() -> None:
    """Changes canvas to general youtube search mode"""
    
    clear_canvas()
    
    canvas["background"] = "#ff0000"
    canvas.update()

def clear_canvas() -> None:
    """Loops through and deletes objects stored as children of canvas. """
    canvas.delete("all")
    for child in canvas.winfo_children():
        child.destroy()

def clear_thumbnails() -> None:
    """Properly closes temp files of all Thumbnail_Image objects. Unlinks reference to all Thumbnail_Image objects."""
    global THUMBNAILS_LIST

    for thumbnail in THUMBNAILS_LIST:
        thumbnail.destroy()
    
    THUMBNAILS_LIST = []


#Download button and his homie functions
def download_button() -> None:
    """Places download button on app. Also contains download function."""

    def download() -> None:
        path = retrieve_path()
        video_id, alt_video_id = retrieve_video()
        video = [video_id, alt_video_id]
        
        download_videos(video, path= path)
    
    tkinter.Button(root, text = "DOWNLOAD", name = "download", width = 50, height = 2, 
                    command = download).place(x = 25, y = 450)


def retrieve_key() -> str:
    """Retrieves the input from API Input entry field"""
    return str(find_widgets_by_name("api_input").get())

def retrieve_path() -> str:
    """Retrieves the input from download path entry field"""
    return str(find_widgets_by_name("path").get())

def retrieve_video() -> Tuple[str,str]:
    """Calls regex to find video id from an inputted video link. Returns a tuple of video ids from input and parsed from link, respectively. """
    video_id_input = find_canvas_widget_by_name("video id").get()      
    video_link_input = find_canvas_widget_by_name("video link").get()
    
    regex_pattern = r"\?v=(.{11})"
    capture_groups = re.search(regex_pattern, video_link_input) 
    video_link_id = capture_groups[0][3:]

    return (video_id_input, video_link_id)

def find_widgets_by_name(name: str):
    """Returns the widget that was named in input."""
    return root.children[name]

def find_canvas_widget_by_name(name:str):
    return root.children["canvas"].children[name]


#Helpful photo friends
def resize_image(image_location: str, height: int, width: int):
    """Given file location, and height/width inputs, shrinks image by a factor of the input. Ex: Current = 120 and 90, input = 10,10 -> result = 12, 9. Returns resized image. """
    image = tkinter.PhotoImage(file = image_location)

    w_scale = int(int(image.width())/width)
    h_scale = int(int(image.height())/height)

    new_image = image.subsample(w_scale,h_scale)

    return new_image

def swap_entry_mode() -> None:
    """Swaps image on secret_button from open to closed eye. 
    Changes display of api_input from * to regular. 
    Returns None."""
    global EYE_OPEN_IMAGE
    global EYE_CLOSED_IMAGE
    global EYE_MODE

    button = find_widgets_by_name("secret_button")
    api_entry =  find_widgets_by_name("api_input")

    if EYE_MODE == 0:
        #Close eye
        button["image"] = EYE_OPEN_IMAGE
        EYE_MODE = 1 
        api_entry.config(show = "*")
    elif EYE_MODE == 1:
        #Open eye
        button["image"] = EYE_CLOSED_IMAGE
        EYE_MODE = 0
        api_entry.config(show ="")
    
    #Show does not change the contents of the entry input.

def globalize_images() -> None:
    """Resizes permanent images. Returns None."""
    global EYE_OPEN_IMAGE
    global EYE_CLOSED_IMAGE

    EYE_OPEN_IMAGE = resize_image("password eye open.png", 20, 20)
    EYE_CLOSED_IMAGE = resize_image("password eye closed.png", 20, 20 )

#Experiment bois
def test_button():
    def print_widget(name: str):
        print(find_widgets_by_name(name).get())

    #tkinter.Button(root, text = "test", command = partial(print_widget, name = "api_input")).place(x= 400, y = 100)


def enumyrate(iterable: Iterable):
    counter = 0
    for x in iterable:
        yield counter, x
        counter +=1


#The main man :DD
def main():
    globalize_images()
    init_screen()

    test_button()
    mode_buttons()
    show_mode()
    download_button()

    root.mainloop()

if __name__ == "__main__":
    main()