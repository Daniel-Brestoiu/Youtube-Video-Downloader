import re
import urllib.request
import tempfile
import tkinter
import ffmpeg_script
import api_logic
import typing

from pathlib import Path
from tkinter import filedialog, messagebox, ttk, font
from ffmpeg_script import *
from api_logic import *
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

VIDEOS_LISTED = []

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
        self.image = ImageTk.PhotoImage(Image.open(self.temp_file.name))
    
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

class Error():
    def __init__(self, master = root, title:str = "Error", message:str = "Error", name:str = None, frame = None, x_pos = None, y_pos = None):
        self.master = master
        self.title = title
        self.message = message
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos

    def popup(self):
        global SEARCH_TYPE

        def place_frame_math(self):
            """Conducts the math necessary to place popup on canvas (in a pretty way :D)"""

            my_font = font.Font(family = "Helevetica", size = 13)   #Default is most likely the same font/size as this 
            text_length = my_font.measure(self.message)             # Gets text message width

            message = tkinter.Text(font = my_font)
            message.insert("end", self.message,)                    # Gets text message height

            width = text_length                      
            height = 3 * message.cget("height")             # 3 lines of text, presumably same message height
            
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            x = (canvas_width - width)//2 - 15             # Necessary shift of 15 to account for X button.
            y = (canvas_height - height)//2 

            self.x_pos = x
            self.y_pos = y

        def move_self(self):

            self.frame.place(x = self.x_pos, y = self.y_pos)
            canvas.update()

        def kill_by_name(self):
            try:
                fake = find_canvas_widget_by_name(self.name)
                fake.kill_self(fake)
            except:
                #Means this is the first error popup. Others do have not been made yet.
                pass

        mode = SEARCH_TYPE.get()
        if mode == 1:
            colour = "#ffc3a9"
        elif mode == 2:
            colour = "#ffd8a9"
        else:
            colour = "#ffada9"

        
        kill_by_name(self.name) #Removes others with same name. All popups have same name (so far)

        self.frame = tkinter.Frame(master = canvas, name = self.name, bg = colour, relief = "solid", borderwidth = 2,)

        exit_button = tkinter.Button(master= self.frame, text = "X",  command = self.kill_self, highlightbackground = colour,).grid(row = 1, column = 3)       #.place(x = 130, y = 2)
        error_title = tkinter.Label(master = self.frame, text = self.title, bg = colour).grid(row = 1, column = 1)       #.place(x = 5, y = 5)
        filler = tkinter.Label(master = self.frame, text = "", bg = colour).grid(row= 2, column = 1)
        error_message = tkinter.Label(master = self.frame, text = self.message, bg = colour, ).grid(row = 3, column = 1)     #.place(x= 25, y = 25)

        place_frame_math(self)
        move_self(self)

    def kill_self(self):
        self.frame.pack_forget()
        self.frame.destroy()

    #Mode 1 popup colour #ffc3a9
    #Mode 2 popup colour #ffd8a9
    #Mode 3 popup colour #ffada9

class Video():
    def __init__(self,  master:canvas, video_id:str, thumbnail:Thumbnail_Image = None, name:str = None, channel:str = None, selected = True, yes_photo = None, no_photo = None, x:int = 0, y:int = 0, colour = None, video_canvas:canvas = None):
        self.master = master
        self.video_id = video_id
        self.thumbnail = thumbnail
        self.name = name
        self.channel = channel
        self.selected = selected
        self.yes_photo = yes_photo
        self.no_photo = no_photo
        self.colour = colour
        self.x = x
        self.y = y
        self.video_canvas = video_canvas

        #Getting Thumbnail
        thumbnail = Thumbnail_Image(url = f"https://img.youtube.com/vi/{self.video_id}/default.jpg")
        thumbnail.download_from_url()
        self.thumbnail = thumbnail

        #Making check and x buttons' image
        self.yes_photo = resize_image("check_mark.png", 10, 10)
        self.no_photo = resize_image("x_mark.png", 10, 10)

        #Setting background
        current_mode = SEARCH_TYPE.get()
        if current_mode == 2:
            self.colour = "#e4e0ff"
        elif current_mode == 3:
            self.colour = "#ebffef"
        #Colours: Mode2: "#b2a9ff"          Mode3: "#a9ffbc"
        #Colours: Mode2: "#e4e0ff"          Mode3: "#ebffef"

    def get_video(self):
        return_value = search_video(video_id = self.video_id, API_KEY= retrieve_key())
        
        if return_value == "Invalid API Key":
            error = Error(message = "Please input a valid Youtube V3 Data Api Key.", name = "popup")
            error.popup()
            return
        elif return_value == "Invalid Video Info":
            error = Error(message = "Please input valid video information.", name = "popup")
            error.popup()
            return
        else:
            title, channel_name, thumbnail_link, thumbnail_width, thumbnail_height = return_value

        self.name = title
        self.channel = channel_name

    def draw_self(self):
        self.video_canvas = tkinter.Canvas(self.master, width = 430, height = 100, bg = self.colour, highlightthickness = 0, bd = 1, relief = "ridge",)
        self.master.create_window((self.x -66, self.y), window = self.video_canvas, width = 430, height = 100, anchor = "w")

        self.video_canvas.create_image((70- 5, 55 - 5), image = self.thumbnail.image)
        self.video_canvas.create_text((70 + 65, 55 - 25), text = self.name, anchor = "w",)
        self.video_canvas.create_text((70 + 65, 55), text = self.channel, anchor = "w",)

        MODES = [(self.yes_photo, "1"),
                (self.no_photo, "2")]
        variable = tkinter.StringVar()
        variable.set("1")
        self.selected = variable

        for image, mode in MODES:
            button = tkinter.Radiobutton(master= self.video_canvas, image = image, variable = variable, value = mode, bg = self.colour, command = self.check_printable,)
            button.place(x = 70 + 320, y = 55 + 20*int(mode) - 30)

        self.master.update()

    def destroy_temp_file(self):
        self.thumbnail.destroy()
    
    
    def check_printable(self):
        return self.selected.get()

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

        return_value = search_video(video_id = video_id, video_link = video_link, API_KEY= api_key_input)
        
        if return_value == "Invalid API Key":
            error = Error(message = "Please input a valid Youtube V3 Data Api Key.", name = "popup")
            error.popup()
            return

        elif return_value == "Invalid Video Info":
            error = Error(message = "Please input valid video information.", name = "popup")
            error.popup()
            return
        else:
            title, channel_name, thumbnail_link, thumbnail_width, thumbnail_height = return_value
        
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
    # Searching by channel and channel ID is inconsistent on youtube API, will not include as feature
    # Search by playlist ID, and link to a video in the playlist.
    # Creates scroll box of the videos in playlist, including thumbnail, name, channel, and a check/x box for including in downloads
    global VIDEOS_LISTED

    def search():
        global VIDEOS_LISTED
        id_input = find_canvas_widget_by_name("playlist id input").get()
        link_input = find_canvas_widget_by_name("playlist link input").get()
        api_key_input = find_widgets_by_name("api_input").get()
        
        link_id = parse_for_playlist_id(link_input)

        result = find_playlist(API_KEY = api_key_input, playlist_id = id_input, playlist_link_id =  link_id)
        
        if result[0] == "Invalid API Key":
            error = Error(message = "Please input a valid Youtube V3 Data Api Key.", name = "popup")
            error.popup()
            return
        elif result[0] == "Invalid Playlist Id":
            error = Error(message = "Please input valid playlist information.", name = "popup")
            error.popup()
            return
        else:
            #No invalid input, result must make sense
            num_videos = len(result)
            # print(result)

            #7 + 100 pixels for padding for each video, + 7 padding at the very end
            height_of_scroll_field = 105*num_videos + 4
            close_scroll_field_temp()
            delete_scroll_field()
            make_scroll_field(x= 20, y= 130, height = height_of_scroll_field)

            VIDEOS_LISTED = []
            for num in range(len(result)):
                video_id = result[num]
                # print(video_id)

                secondary_canvas = find_canvas_widget_by_name("holder frame").children["secondary canvas"]

                video = Video(master = secondary_canvas, video_id = video_id, x = 70, y = 55 + 105*num)
                video.get_video()
                video.draw_self()

                VIDEOS_LISTED.append(video)

            # print(VIDEOS_LISTED)            

    clear_canvas()
    canvas["background"] = "#b2a9ff"    

    tkinter.Label(canvas, name = "playlist id label", text = "Playlist ID:", width = 10, anchor = "w", bg = "#b2a9ff").place(x= 20, y= 22)
    tkinter.Label(canvas, name = "playlist link", text = "Playlist Link:", width = 10, anchor = "w", bg = "#b2a9ff").place(x= 20, y= 56)

    tkinter.Entry(canvas, name = "playlist id input", width = 39).place(x= 110, y= 20)
    tkinter.Entry(canvas, name = "playlist link input", width = 39).place(x= 110, y= 54)

    tkinter.Button(canvas, name = "search by playlist button", text = "SEARCH", width = 50, height = 2, command = search).place(x= 20, y = 90)

    make_scroll_field(x = 20, y = 130, height= 300)
    canvas.update()

def make_scroll_field(x, y, height):

    colour1 = "#aaaaaa"
    colour2 = "#aaaaaa"

    if SEARCH_TYPE.get() == 2:
        colour1 = "#a696ff"
        colour2 = "#e3d4ff"
    elif SEARCH_TYPE.get() == 3:
        colour1 = "#a9ffbc"
        colour2 = "#d4fff7"
        

    holder_frame = tkinter.Canvas(canvas, name = "holder frame", bg = colour1, width = 455, height = 170, bd = 0, highlightthickness = 0, )
    holder_frame.place(x = x, y = y)

    secondary_canvas = tkinter.Canvas(holder_frame, name = "secondary canvas", bg= colour1 , width = 440, height = 170, bd = 0, highlightthickness = 0,)
    secondary_canvas.pack(side = "left", fill = "both")
    secondary_canvas.create_rectangle( 0, 0, 438, height, fill = colour2, outline = "")

    scroll_bar = tkinter.Scrollbar(master = holder_frame, orient = "vertical", name = "scroll bar", bg = colour2 )
    scroll_bar.pack(side = "right", fill = "y")
    scroll_bar.config(command = secondary_canvas.yview)
    secondary_canvas.config(yscrollcommand= scroll_bar.set)
    secondary_canvas.configure(scrollregion = secondary_canvas.bbox("all"))


def youtube_search_screen() -> None:
    """Changes canvas to general youtube search mode"""
    
    clear_canvas()
    
    canvas["background"] = "#a9ffbc"

    make_scroll_field(x = 20, y = 130, height = 300)

    canvas.update()

def close_scroll_field_temp() -> None:
    for video in VIDEOS_LISTED:
        video.destroy_temp_file()
        # print(f"Temp for {video} is destroyed")

def delete_scroll_field() -> None:
    holder_frame = find_canvas_widget_by_name("holder frame")
    holder_frame.destroy()
    
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

    def download_video() -> None:
        path = retrieve_path()
        video = retrieve_video()
        
        if video == "Invalid Video Info":
            error = Error(message = "Please input valid video information.", name = "popup")
            error.popup()
            return
        elif path == "":
            error = Error(title = "Warning!", message = f"Default download location selected: {Path.home()}", name = "popup")            
            error.popup()
            root.update()

        download_videos(video, path= path)

    def download_playlist() -> None:
        pass

    def download_search() -> None:
        pass
    
    tkinter.Button(root, text = "DOWNLOAD", name = "download", width = 50, height = 2, 
                    command = download_video).place(x = 25, y = 450)


def retrieve_key() -> str:
    """Retrieves the input from API Input entry field"""
    return str(find_widgets_by_name("api_input").get())

def retrieve_path() -> str:
    """Retrieves the input from download path entry field"""
    return str(find_widgets_by_name("path").get())

def retrieve_video() -> Tuple[str,str]:
    """Calls regex to find video id from an inputted video link. Returns a tuple of video ids from input and parsed from link, respectively. """
    
    try:
        video_id_input = find_canvas_widget_by_name("video id").get()      
        video_link_input = find_canvas_widget_by_name("video link").get()
        
        regex_pattern = r"\?v=(.{11})"
        capture_groups = re.search(regex_pattern, video_link_input) 
        video_link_id = capture_groups[0][3:]
    except:
        return "Invalid Video Info"

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

def make_video_display(master:canvas, video_id:str, x:int, y:int):
    video = Video(master = master, video_id = video_id, x = x, y = y)
    video.get_video()
    video.draw_self()

#Experiment bois
def test_button():
    def print_widget(name: str):
        #DEPRECATED
        print(find_widgets_by_name(name).get())

    def place_video():
        #DEPRECATED
        secondary_canvas = find_canvas_widget_by_name("holder frame").children["secondary canvas"]

        test_video = Video(master = secondary_canvas, video_id = "wHAFcQY7PbM", x = 70, y = 55)
        test_video.get_video()
        test_video.draw_self()
    
    # tkinter.Button(root, text = "test", command = partial(print_widget, name = "api_input")).place(x= 400, y = 100)
    
    # error = Error(message= "This is a sample of what an error message might be" , name = "popup")
    # tkinter.Button(root, text = "test", command = place_video).place(x= 400, y = 100)

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