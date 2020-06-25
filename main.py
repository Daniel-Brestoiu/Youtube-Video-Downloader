import googleapiclient
from googleapiclient.discovery import build
from ffmpeg_script import download_videos

"""
To Do:
    - Download videos using FFmpeg and video ID
        - Verify they haven't been downloaded already
        - To find a video, https://www.youtube.com/watch?v=(videoId)        
    - Store video ID's of downloaded videos
    - Add to media player?

Channel UCrS7pF40yRheVTFXzuawvwA
Playlist PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG
"""


API_key = 'AIzaSyBs1qMkQYzS4Vr2oCBYHOfx_TTcM6xYGUk'
youtube = build("youtube", "v3", developerKey=API_key)


def query(search_item):
    """ Search youtube for input parameter.
        Returns list of 5 results and their video IDs,"""
        
    request = youtube.search().list(q=str(search_item), 
                                    part="snippet",
                                    type="video")  # type --> googleapiclient.http.HttpRequest
    result = request.execute()

    results_list = []
    for item in result["items"]:
        results_list.append((item['snippet']["title"], item["id"]["videoId"]))

    return(results_list)


def find_videos_in_playlist():
    """Finds specific, existing playlist where I put youtube video songs I liked.
    Returns video Id for each of the videos in a list."""

    playlist = youtube.playlistItems().list(part="contentDetails",
                                            playlistId="PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG").execute()

    videos_list = []
    for video in (playlist["items"]):
        videos_list.append(video["contentDetails"]["videoId"])

    return(videos_list)


def check_file_codes(file_name):
    """Opens or Creates a file named after input parameter. 
    Reads the lines of the file, returning list of enter separated lines."""

    try:
        handle = open(str(file_name), "r")
    except:
        new_file = open(str(file_name), "x")
        new_file.close()
        print("Made new file.")
        handle = open(str(file_name), "r")

    file_contents = handle.readlines()

    downloaded_codes = []
    for line in file_contents:
        downloaded_codes.append(line.rstrip())

    handle.close()

    return(downloaded_codes)


def cull_codes(video_codes, downloaded_codes):
    """Given two lists of strings, where the second list is a subset of the first, returns the first list without the subset."""

    unique_codes = []

    for x in video_codes:
        if x not in downloaded_codes:
            unique_codes.append(x)

    return (unique_codes)


def find_unique_codes(new_video_codes):
    """Given list, returns a subset of the list which does not contain duplicates from a known file, downloads.txt"""

    unique_codes = cull_codes(new_video_codes, check_file_codes("downloads.txt"))
    return (unique_codes)


def write_to_file(file_name, codes_list):
    """Given file name and a list, appends to the file all items in the list as a string."""

    file_handle = open(str(file_name), "a")

    for _ in codes_list:
        file_handle.write(_ + "\n")

    file_handle.close()


if __name__ == "__main__":
    codes = find_unique_codes(find_videos_in_playlist())
    write_to_file("downloads.txt", codes)
    download_videos(codes)
