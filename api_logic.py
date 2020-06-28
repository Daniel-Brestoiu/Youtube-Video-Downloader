import googleapiclient
from googleapiclient.discovery import build
from ffmpeg_script import download_videos
from typing import Tuple, List

"""
Channel UCrS7pF40yRheVTFXzuawvwA
Playlist PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG
"""


API_KEY = 'AIzaSyBs1qMkQYzS4Vr2oCBYHOfx_TTcM6xYGUk'
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)


def query(search_item: str) -> List[Tuple[str, str]]:
    """ Search youtube for input parameter.
        Returns list of 5 results and their video IDs
    """

    assert type(search_item) == str, "Improper search code"

    request: googleapiclient.http.HttpRequest = YOUTUBE.search().list(q=search_item,
                                                                      part="snippet",
                                                                      type="video")
    result = request.execute()

    results_list: List[Tuple[str, str]] = []
    for item in result["items"]:
        results_list.append((item['snippet']["title"], item["id"]["videoId"]))

    return results_list


def find_videos_in_playlist(playlistID: str) -> List[str]:
    """Finds specific, existing playlist where I put youtube video songs I liked.
    Returns video Id for each of the videos in a list."""

    playlist = YOUTUBE.playlistItems().list(part="contentDetails",
                                            playlistId=playlistID).execute()

    videos_list: List[str] = []
    for video in (playlist["items"]):
        videos_list.append(video["contentDetails"]["videoId"])

    return videos_list


def check_file_codes(file_name: str) -> List[str]:
    """Opens or Creates a file named after input parameter. 
    Reads the lines of the file, returning list of enter separated lines."""

    assert type(file_name) == str, "Improper file name input."

    try:
        handle = open(file_name, "r")
    except:
        new_file = open(file_name, "x")
        new_file.close()
        print("Made new file.")
        handle = open(file_name, "r")

    file_contents = handle.readlines()

    downloaded_codes: List[str] = []
    for line in file_contents:
        downloaded_codes.append(line.rstrip())

    handle.close()

    return downloaded_codes


def cull_codes(video_codes: List[str], downloaded_codes: List[str]) -> List[str]:
    """Given two lists of strings, where the second list is a subset of the first, returns the first list without the subset."""

    unique_codes = []

    for x in video_codes:
        if x not in downloaded_codes:
            unique_codes.append(x)

    return unique_codes


def find_unique_codes(new_video_codes: List[str]) -> List[str]:
    """Given list, returns a subset of the list which does not contain duplicates from a known file, downloads.txt"""

    unique_codes = cull_codes(new_video_codes, check_file_codes("downloads.txt"))
    return unique_codes


def write_to_file(file_name: str, codes_list: List[str]) -> None:
    """Given file name and a list, appends to the file all items in the list as a string."""

    file_handle = open(file_name, "a")

    for x in codes_list:
        file_handle.write(x + "\n")

    file_handle.close()

def main() -> None:
    codes = find_unique_codes(find_videos_in_playlist("PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG"))
    write_to_file("downloads.txt", codes)
    download_videos(codes)


if __name__ == "__main__":
    main()