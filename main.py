import googleapiclient
from googleapiclient.discovery import build


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
youtube = build("youtube", "v3", developerKey= API_key)


def query(search_item):
    """ Search youtube for input parameter.
        Returns list of 5 results and their video IDs,"""
    request = youtube.search().list(q= str(search_item), part = "snippet", type = "video")      #type --> googleapiclient.http.HttpRequest
    result = request.execute()

    results_list = []
    for item in result["items"]:
        results_list.append((item['snippet']["title"], item["id"]["videoId"]))
        
    return(results_list)


def find_videos_in_playlist():
    playlist = youtube.playlistItems().list(part = "contentDetails",  playlistId = "PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG").execute()

    videos_list = []
    for video in (playlist["items"]):
        videos_list.append(video["contentDetails"]["videoId"])

    return(videos_list)



if __name__ == "__main__":
    print(find_videos_in_playlist())
