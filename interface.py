import tkinter
import ffmpeg_script
import urllib.request

import api_logic
from api_logic import search_video

import typing
from typing import List, Tuple, Iterable

from functools import partial
from PIL import Image, ImageTk

global search_type
global photo
photo = Image.open("placeholder_image.png")

root = tkinter.Tk()
canvas = tkinter.Canvas(root, name = "canvas", width = 485, height = 300, )
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

    tkinter.Entry(root, name = "api_input", width = 39).place(x = 130, y = 10)
    tkinter.Entry(root, name = "path", width = 39).place(x= 130, y = 50)
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
    global photo

    def search() -> None:
        global photo

        video_id = get_video_id()
        video_link = get_video_link()

        title, channel_name, thumbnail_link, thumbnail_width, thumbnail_height = search_video(video_id = video_id, video_link = video_link)

        find_canvas_widget_by_name("video found label")["text"] = title
        find_canvas_widget_by_name("youtuber of video label")["text"] = channel_name

        download_location = download_to_temp(thumbnail_link, title)

        photo = ImageTk.PhotoImage(Image.open(download_location))
        thumbnail_placeholder = canvas.create_image((scale/2 + 20,scale/2 + 5), image = photo)

        canvas.update()
        

    def get_video_id() -> str:
        return find_canvas_widget_by_name("video id").get()

    def get_video_link() -> str:
        return find_canvas_widget_by_name("video link").get()


    canvas.delete("all")
    clear_canvas()

    canvas["background"] = "#A9EDFF"

    scale = 100
    photo = resize_image("placeholder_image.png", scale, scale)
    thumbnail_placeholder = canvas.create_image((scale/2 + 5,scale/2 + 5), image = photo)


    tkinter.Label(canvas, name = "video id label", text = "Video ID:", width = 10, anchor = "w", bg = "#A9EDFF",).place(x = 17, y = 124)
    tkinter.Label(canvas, name = "video link label", text = "Video Link:", width = 10, anchor = "w", bg = "#A9EDFF",).place(x= 17, y = 164) 
    tkinter.Label(canvas, name = "video found label", text = "No Video Searched Yet", bg = "#A9EDFF", width = 38, anchor = "w",).place(x =145, y = 25)
    tkinter.Label(canvas, name = "youtuber of video label", text = "No Channel Posted This Video", bg = "#A9EDFF", width = 38, anchor = "w").place(x = 145, y = 55)
    tkinter.Label(canvas, name = "instructions label", text = "Provide input then click search. Download if correct video is found.", bg = "#A9EDFF", anchor = "w").place(x = 20, y = 220)

    tkinter.Entry(canvas, name = "video id", width = 40).place(x = 100, y = 125)
    tkinter.Entry(canvas, name = "video link", width = 40).place(x = 100, y = 165)

    tkinter.Button(canvas, name = "search by video button", text = "SEARCH", width = 50, height = 2, 
                    command = search).place(x= 20, y = 250)

    canvas.update()




def playlist_search_screen():
    """Changes canvas to playlist search mode"""
    
    canvas.delete("all")
    clear_canvas()

    canvas["background"] = "#09ff00"
    
    
    
    canvas.update()
    

def youtube_search_screen():
    """Changes canvas to general youtube search mode"""
    
    canvas.delete("all")
    clear_canvas()
    
    canvas["background"] = "#ff0000"
    
    
    
    canvas.update()

def clear_canvas():
    for child in canvas.winfo_children():
        child.destroy()




#Download button and his homie functions
def download_button():

    def download() -> None:
        key = retrieve_key()
        path = retrieve_path()
        video = retrieve_video()

        print(key, path, video)

    tkinter.Button(root, text = "DOWNLOAD", name = "download", width = 50, height = 2, 
                    command = download).place(x = 25, y = 450)


def retrieve_key() -> str:
    """Retrieves the input from API Input entry field"""
    
    return str(find_widgets_by_name("api_input").get())

def retrieve_path() -> str:
    """Retrieves the input from download path entry field"""
    return str(find_widgets_by_name("path").get())

def retrieve_video():
    pass       

def find_widgets_by_name(name: str):
    """Returns the widget that was named in input."""
    return root.children[name]

def find_canvas_widget_by_name(name:str):
    return root.children["canvas"].children[name]



#Helpful photo friends
def resize_image(image_location: str, height: int, width: int):
    image = tkinter.PhotoImage(file = image_location)

    w_scale = int(int(image.width())/width)
    h_scale = int(int(image.height())/height)

    new_image = image.subsample(w_scale,h_scale)

    return new_image

def download_to_temp(image_url: str, title: str) -> str:
    """Given a network object denotated by a URL, downloads to file and returns path to newly downloaded file."""
    
    thumbnail_name = "temp thumbnails/" + title + " thumbnail.jpg"

    path, http_message = urllib.request.urlretrieve(url = image_url, filename= thumbnail_name)

    return str(path)


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