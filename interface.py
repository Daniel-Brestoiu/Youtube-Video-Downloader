import re
import urllib.request
import tempfile
import tkinter
import ffmpeg_script
import api_logic
import typing
import time

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
    def __init__(self, url: str = None, temp_file: IO[Any] = None, scale: int = None, width: int = None, height: int = None, image: tkinter.PhotoImage = None, overlord = None):
        global THUMBNAILS_LIST

        self.url = url
        self.temp_file = temp_file
        self.scale = scale
        self.width = width
        self.height = height
        self.image = image
        self.overlord = overlord

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
    def __init__(self, master = root, title:str = "Error", message:str = "Error", name:str = None, frame: tkinter.Frame = None, x_pos:int = None, y_pos:int = None):
        self.master = master
        self.title = title
        self.message = message
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos

    def popup(self) -> None:
        global SEARCH_TYPE

        def place_frame_math(self) -> None:
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

        def move_self(self) -> None:
            """Places self at given x and y co-ordinates"""

            self.frame.place(x = self.x_pos, y = self.y_pos)
            canvas.update()

        def kill_by_name(self) -> None:
            """Eliminated other objects with same name. All Error obj should have same name; 'popup' """
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

        
        kill_by_name(self.name)

        self.frame = tkinter.Frame(master = canvas, name = self.name, bg = colour, relief = "solid", borderwidth = 2,)

        exit_button = tkinter.Button(master= self.frame, text = "X",  command = self.kill_self, highlightbackground = colour,).grid(row = 1, column = 3)       #.place(x = 130, y = 2)
        error_title = tkinter.Label(master = self.frame, text = self.title, bg = colour).grid(row = 1, column = 1)
        filler = tkinter.Label(master = self.frame, text = "", bg = colour).grid(row= 2, column = 1)
        error_message = tkinter.Label(master = self.frame, text = self.message, bg = colour, ).grid(row = 3, column = 1)

        place_frame_math(self)
        move_self(self)

    def kill_self(self) -> None:
        """Eliminates own existance."""
        self.frame.pack_forget()
        self.frame.destroy()

    #Mode 1 popup colour #ffc3a9
    #Mode 2 popup colour #ffd8a9
    #Mode 3 popup colour #ffada9

class Video():
    def __init__(self,  master:canvas, video_id:str, thumbnail:Thumbnail_Image = None, name:str = None, channel:str = None, selected:str = "1", yes_photo: tkinter.PhotoImage = None, no_photo: tkinter.PhotoImage = None, x:int = 0, y:int = 0, colour:str = None, video_canvas:canvas = None):
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
        thumbnail = Thumbnail_Image(url = f"https://img.youtube.com/vi/{self.video_id}/default.jpg", overlord = self)
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

    def get_video(self) -> None:
        """Conducts the search for video, updating information about self, or causing error popup."""
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

    def draw_self(self) -> None:
        """Creates canvas, and draws self on it. Results in rectangular box with thumbnail image, name, channel, and buttons. """
        self.video_canvas = tkinter.Canvas(self.master, width = 430, height = 100, bg = self.colour, highlightthickness = 0, bd = 1, relief = "ridge",)
        self.master.create_window((self.x -66, self.y), window = self.video_canvas, width = 430, height = 100, anchor = "w")

        self.video_canvas.create_image((70- 5, 55 - 5), image = self.thumbnail.image)
        self.video_canvas.create_text((70 + 65, 55 - 25), text = self.name, anchor = "w",)
        self.video_canvas.create_text((70 + 65, 55), text = self.channel, anchor = "w",)

        MODES = [(self.yes_photo, "1"),
                (self.no_photo, "2")]
        variable = tkinter.StringVar()
        variable.set(self.selected)
        self.selected = variable

        for image, mode in MODES:
            button = tkinter.Radiobutton(master= self.video_canvas, image = image, variable = variable, value = mode, bg = self.colour, command = self.check_printable,)
            button.place(x = 70 + 320, y = 55 + 20*int(mode) - 30)

        self.master.update()

    def destroy_temp_file(self) -> None:
        """ Proper elimination of thumbnail and temp file of video's associated thumbnail image."""
        self.thumbnail.destroy()
    
    def check_printable(self) -> str:
        """Returns value for a video's selected attribute. This will be either 1 or 2, representing yes and no respectively."""
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
    tkinter.Button(root, name = "help button", text = "HELP", width = 5, pady= 5, command= help_me).place(x= 445, y = 97)

def select_path() -> None:
    """Opens popup prompting user to pick a directory. Fills 'path' entry widget with path."""

    root.update()
    directory = str(tkinter.filedialog.askdirectory(title= "Download Path Selection", parent= root))
    root.update()
   
    entry = find_widgets_by_name("path")
    entry.delete(0, "end")
    entry.insert(0, directory)

def help_me() -> None:
    """ Makes a new window which is used to display help instructions."""

    def popup_message(msg):
        norm_font = ("Helvetica", 13)
        
        pop_up = tkinter.Tk()
        pop_up.wm_title("Helper")
        label = tkinter.Label(pop_up, text = msg, font = norm_font, width = 75, height = 25)

        label.pack(side= "right", fill = "x", pady = 10)

    message = """
    Instructions: 
    Get an API Key with https://developers.google.com/youtube/v3/getting-started
    Follow the instruction at the link, then input a Youtube V3 youtube API key 
    Use to "Browse" button to select a download location

    Video mode:
    Provide a youtube video ID or link. 
    Use the "SEARCH" button (optional), then download.
    *Note: In this mode the user can download without an API key. 
    **Note: Without an API key, the "SEARCH" button will be non-functional.

    Playlist mode:
    Input youtube playlist ID or link.
    Click the "SEARCH" button to find the playlist.
    Change the check mark to "X" to not download a video.
    Click the "DOWNLOAD" button to download all wanted videos.

    Search mode:
    Search for videos using the search bar. 
    Click the "SEARCH" button, and wait for results.
    Scroll through the results, and find the video you wanted to download.
    On the wanted video, change the "X" button to the check mark, then click "DOWNLOAD"
    """
    popup_message(message)

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
        """ Conducts search for a video, using api_logic import. Pops up error if applicable, otherwise updates thumbnail image, video title and channel name"""

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
    tkinter.Label(canvas, name = "instructions label", text = "Provide input then click search. Download if correct video is found.", bg = "#A9EDFF", anchor = "w").place(x = 40, y = 220)

    tkinter.Entry(canvas, name = "video id", width = 40).place(x = 100, y = 125)
    tkinter.Entry(canvas, name = "video link", width = 40).place(x = 100, y = 165)

    tkinter.Button(canvas, name = "search by video button", text = "SEARCH", width = 50, height = 2, 
                    command = search).place(x= 20, y = 250)

    canvas.update()


def playlist_search_screen() -> None:
    """Changes canvas to playlist search mode"""
    # Search by playlist ID, and link to a video in the playlist.
    # Creates scroll box of the videos in playlist, including thumbnail, name, channel, and a check/x box for including in downloads
    global VIDEOS_LISTED

    def search() -> None:
        """ Conducts search for youtube playlist, popping up an error if applicable. Otherwise kills previous scroll field, and
        creates a new, resized one which hosts all the videos of the playlist. Pops up completion poppup.  """

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
            num_videos = len(result)

            #7 + 100 pixels for padding for each video, + 7 padding at the very end
            height_of_scroll_field = 105*num_videos + 4

            clear_thumbnails()
            delete_scroll_field()

            make_scroll_field(x= 20, y= 130, scroll_height = height_of_scroll_field)

            VIDEOS_LISTED = []
            for num in range(len(result)):
                video_id = result[num]

                secondary_canvas = find_canvas_widget_by_name("holder frame").children["secondary canvas"]

                video = Video(master = secondary_canvas, video_id = video_id, x = 70, y = 55 + 105*num)
                video.get_video()
                video.draw_self()

                VIDEOS_LISTED.append(video)

            popup = Error(message = "Playlist Search complete! :D", title = "Good news!", name = "popup")      
            popup.popup()

    clear_canvas()
    canvas["background"] = "#b2a9ff"    

    tkinter.Label(canvas, name = "playlist id label", text = "Playlist ID:", width = 10, anchor = "w", bg = "#b2a9ff").place(x= 20, y= 22)
    tkinter.Label(canvas, name = "playlist link", text = "Playlist Link:", width = 10, anchor = "w", bg = "#b2a9ff").place(x= 20, y= 56)

    tkinter.Entry(canvas, name = "playlist id input", width = 39).place(x= 110, y= 20)
    tkinter.Entry(canvas, name = "playlist link input", width = 39).place(x= 110, y= 54)

    tkinter.Button(canvas, name = "search by playlist button", text = "SEARCH", width = 50, height = 2, command = search).place(x= 20, y = 90)

    make_scroll_field(x = 20, y = 130, scroll_height= 300)
    canvas.update()

def make_scroll_field(x:int, y:int, scroll_height:int, height:int = 170) -> None:
    """ Given information for position, scroll depth and height, creates what amounts to a scrollable canvas as specified in input parameters. """

    colour1 = "#aaaaaa"
    colour2 = "#aaaaaa"

    if SEARCH_TYPE.get() == 2:
        colour1 = "#b2a9ff"
        colour2 = "#e3d4ff"
    elif SEARCH_TYPE.get() == 3:
        colour1 = "#a9ffbc"
        colour2 = "#d4fff7"
        

    holder_frame = tkinter.Canvas(canvas, name = "holder frame", bg = colour1, width = 455, height = height, bd = 0, highlightthickness = 0, )
    holder_frame.place(x = x, y = y)

    secondary_canvas = tkinter.Canvas(holder_frame, name = "secondary canvas", bg= colour1 , width = 440, height = height, bd = 0, highlightthickness = 0,)
    secondary_canvas.pack(side = "left", fill = "both")
    secondary_canvas.create_rectangle( 0, 0, 438, scroll_height, fill = colour2, outline = "")

    scroll_bar = tkinter.Scrollbar(master = holder_frame, orient = "vertical", name = "scroll bar", bg = colour2 )
    scroll_bar.pack(side = "right", fill = "y")
    scroll_bar.config(command = secondary_canvas.yview)
    secondary_canvas.config(yscrollcommand= scroll_bar.set)
    secondary_canvas.configure(scrollregion = secondary_canvas.bbox("all"))


def youtube_search_screen() -> None:
    """Changes canvas to general youtube search mode"""
    
    def search() -> None:
        """ Conducts general search query to youtube and displays the found Video objects on scrollable canvas. Finally causes popup indicating completion. """

        global VIDEOS_LISTED
        search_input = find_canvas_widget_by_name(name = "youtube search field").get()
        api_key_input = find_widgets_by_name("api_input").get()
        
        results = query(search_item = search_input, API_KEY = api_key_input) 


        height_of_scroll_field = 105*len(results) + 4

        clear_thumbnails()
        delete_scroll_field()
        make_scroll_field(x= 20, y= 95, scroll_height = height_of_scroll_field, height = 200)

        secondary_canvas = find_canvas_widget_by_name("holder frame").children["secondary canvas"]
        increment = 0
        VIDEOS_LISTED = []

        for (name, video_id) in results:

            video = Video(master = secondary_canvas, video_id = video_id, x = 70, y = 55 + 105*increment, selected = "2")
            video.get_video()
            video.draw_self()
            VIDEOS_LISTED.append(video)

            increment += 1

        popup = Error(message = "Video Search complete! :D", title = "Good news!", name = "popup")      
        popup.popup()

    clear_canvas()
    
    canvas["background"] = "#a9ffbc" 

    make_scroll_field(x = 20, y = 95, scroll_height = 300, height = 200)

    tkinter.Label(canvas, name = "search youtube label", text = "Search Youtube:", bg = "#a9ffbc").place(x= 20,y = 20)
    tkinter.Entry(canvas, name = "youtube search field", width = 36,).place(x = 135, y = 19)
    tkinter.Button(canvas, name = "search by playlist button", text = "SEARCH", width = 50, height = 2, command = search).place(x= 20, y = 55)

    canvas.update()

def delete_scroll_field() -> None:
    """ Finds currently existing scroll field and destroys it, along with its children."""
    clear_thumbnails()
    holder_frame = find_canvas_widget_by_name("holder frame")
    holder_frame.destroy()
    
def clear_canvas() -> None:
    """Loops through and deletes objects stored as children of canvas. """
    clear_thumbnails()

    canvas.delete("all")
    for child in canvas.winfo_children():
        child.destroy()
    

def clear_thumbnails() -> None:
    """Properly closes temp files of all Thumbnail_Image objects. Unlinks reference to all Thumbnail_Image objects."""
    global THUMBNAILS_LIST

    for thumbnail in THUMBNAILS_LIST:
        thumbnail.destroy()
    
    THUMBNAILS_LIST = []


def download_button() -> None:
    """Places download button on app. Also contains download function."""

    def download() -> None:
        """ Figures out which search mode is active, and calls relevant download proceduce"""
        if SEARCH_TYPE.get() == 1:
            download_video()
        elif SEARCH_TYPE.get() == 2:
            download_playlist()
        elif SEARCH_TYPE.get() == 3:
            download_playlist()

    def download_videos_in_playlist(path:str = "") -> None:
        """ Downloads all wanted videos in currently known, listed videos"""

        for video in VIDEOS_LISTED:
            want_download = video.check_printable()

            if want_download == "1":
                ffmpeg_script.download_video(video_code = video.video_id, path = path)

    def download_video() -> None:
        """ Uses known inputs for path and video to download video to location indicated by path. """
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
            canvas.update()
        else:
            message = Error(title = "Don't Worry!", message = "Download has begun.", name = "popup")
            message.popup()
            root.update()
            canvas.update()

        root.after(1000, download_videos(video, path= path))

        popup = Error(message = "Video download complete!", title = "Good news!", name = "popup")
        popup.popup()

    def download_playlist() -> None:
        """ Handles potential errors then calls download_videos_in_playlist() using a known path input """
        path = retrieve_path()

        if len(VIDEOS_LISTED) == 0:
            error = Error(message = "No playlist or videos have been searched!", name = "popup")
            error.popup()
            root.update()
            return
        elif path == "":
            error = Error(title = "Warning!", message = f"Default download location selected: {Path.home()}", name = "popup")            
            error.popup()
            root.update()
        else:
            message = Error(title ="Don't Worry!", message = "Download has begun. Be patient, this may take a while.", name = "popup")
            message.popup()
            root.update()

        root.after(1000, download_videos_in_playlist(path=path))

        popup = Error(message = "Download complete!", title = "Good news!", name = "popup")
        popup.popup()
    
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

    try:
        regex_pattern = r"\?v=(.{11})"
        capture_groups = re.search(regex_pattern, video_link_input) 
        video_link_id = capture_groups[0][3:]
        
        return (video_id_input, video_link_id)
    except:
        #Invalid Link Input
        if len(video_id_input) != 11:
            return "Invalid Video Info"

        return [video_id_input]

    

def find_widgets_by_name(name: str) -> Any:
    """Returns the widget that was named in input."""
    return root.children[name]

def find_canvas_widget_by_name(name:str) -> Any:
    return root.children["canvas"].children[name]


#Helpful photo friends
def resize_image(image_location: str, height: int, width: int) -> tkinter.PhotoImage:
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

def globalize_images() -> None:
    """Resizes permanent images. Returns None."""
    global EYE_OPEN_IMAGE
    global EYE_CLOSED_IMAGE

    EYE_OPEN_IMAGE = resize_image("password eye open.png", 20, 20)
    EYE_CLOSED_IMAGE = resize_image("password eye closed.png", 20, 20 )

def make_video_display(master:canvas, video_id:str, x:int, y:int) -> None:
    video = Video(master = master, video_id = video_id, x = x, y = y)
    video.get_video()
    video.draw_self()

def test_button() -> None:
    """ Deprecated. Previously creates button used to test functions."""
    def print_widget(name: str) -> None:
        #DEPRECATED
        # print(find_widgets_by_name(name).get())
        pass

    def place_video(test_video_id:str) -> None:
        """ Deprecated. """
        secondary_canvas = find_canvas_widget_by_name("holder frame").children["secondary canvas"]

        test_video = Video(master = secondary_canvas, video_id = test_video_id, x = 70, y = 55)
        test_video.get_video()
        test_video.draw_self()
    
    # tkinter.Button(root, text = "test", command = partial(print_widget, name = "api_input")).place(x= 400, y = 100)
    
    # error = Error(message= "This is a sample of what an error message might be" , name = "popup")
    # tkinter.Button(root, text = "test", command = place_video).place(x= 400, y = 100)


def main() -> None:
    """ Program :)"""
    globalize_images()
    init_screen()

    mode_buttons()
    show_mode()
    download_button()

    root.mainloop()

if __name__ == "__main__":
    main()