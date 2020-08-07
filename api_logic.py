import re
import googleapiclient
from pathlib import Path
from googleapiclient.discovery import build
from ffmpeg_script import download_videos
from typing import Tuple, List

def query(search_item: str, API_KEY:str) -> List[Tuple[str, str]]:
    """ Search youtube for input parameter.
        Returns list of 10 results and their video IDs
    """
    YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

    assert type(search_item) == str, "Improper search code"
    request: googleapiclient.http.HttpRequest = YOUTUBE.search().list(q=search_item, part="snippet", type="video", maxResults = 10)
    result = request.execute()

    results_list: List[Tuple[str, str]] = []
    for item in result["items"]:
        results_list.append((item['snippet']["title"], item["id"]["videoId"]))

    return results_list


def find_videos_in_playlist(playlistID: str, API_KEY:str) -> List[str]:
    """Finds specific, existing playlist where I put youtube video songs I liked.
    Returns video Id for each of the videos in a list."""
    
    YOUTUBE = build("youtube", "v3", developerKey=API_KEY)
    playlist = YOUTUBE.playlistItems().list(part="contentDetails",
                                            playlistId=playlistID).execute()

    videos_list: List[str] = []
    for video in (playlist["items"]):
        videos_list.append(video["contentDetails"]["videoId"])

    return videos_list

def search_video(API_KEY:str, video_id: str, video_link: str = None, ) -> List[str]:
    """Given a youtube video identifier, finds the video in question.
    Downloads the video thumbnail as image
    Returns the Video Name, Channel name, thumbnail image name/location?"""
    
    try:
        YOUTUBE = build("youtube", "v3", developerKey=API_KEY)
    except Exception:
        return "Invalid API Key"


    def get_video_info(video_id: str) -> List[str]:
        request = YOUTUBE.videos().list(part = "snippet", id = video_id)
        response = request.execute()

        title = response["items"][0]["snippet"]["title"]
        channel_name = response["items"][0]["snippet"]["channelTitle"]

        thumbnail_link = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        thumbnail_width = response["items"][0]["snippet"]["thumbnails"]["default"]["width"]
        thumbnail_height = response["items"][0]["snippet"]["thumbnails"]["default"]["height"]    

        return [title,channel_name, thumbnail_link, thumbnail_width, thumbnail_height]

    if len(video_id) != 11:
        #print("Invalid video ID input. Searching using link information.")

        try:
            regex_pattern = r"\?v=(.{11})"
            capture_groups = re.search(regex_pattern, string = video_link)
            link_id = capture_groups[0][3:]
            info = get_video_info(link_id)
        except:
            return "Invalid Video Info"

    else:
        #print("Valid video ID input, searching through video ID.")
        
        try:
            request = YOUTUBE.videos().list(part = "snippet", id = video_id)
            response = request.execute()
            
            info = get_video_info(video_id)
            return info

        except:
            try:
                regex_pattern = r"\?v=(.{11})"
                capture_groups = re.search(regex_pattern, string = video_link)
                link_id = capture_groups[0][3:]
                info = get_video_info(link_id)
            except:
                return "Invalid Video Info"

    #Thumbnail at https://img.youtube.com/vi/<insert-youtube-video-id-here>/default.jpg
    return info

def parse_for_playlist_id(playlist_link:str)-> str:
    try:
        regex_pattern = r"list=(.{34})"
        match = re.search(regex_pattern, string = playlist_link)
        link_id = match[0][5:]
        return link_id
    except:
        #Not valid link
        pass
    return None

def find_playlist(API_KEY:str, playlist_id:str , playlist_link_id:str = None) -> List[str]:
    
    try:
        YOUTUBE = build("youtube", "v3", developerKey=API_KEY)
    except Exception:
        return ["Invalid API Key"]

    if len(playlist_id) != 34:
        #Definitely invalid playlist id
        try:
            request = YOUTUBE.playlistItems().list(part="contentDetails", playlistId= playlist_link_id, maxResults = 50) # maxResults = 50
            response = request.execute()

            videos_list = get_next_page(response, YOUTUBE, playlist_link_id)
            if "Done" in videos_list:
                videos_list = []

            for video in (response["items"]):
                videos_list.append(video["contentDetails"]["videoId"])
            return videos_list

        except:
            return ["Invalid Playlist Id"]

    else:
        #Maybe valid playlist id?
        try:
            request = YOUTUBE.playlistItems().list(part="contentDetails", playlistId= playlist_id, maxResults = 50)
            response = request.execute()


            videos_list = get_next_page(response, YOUTUBE, playlist_id)
            if "Done" in videos_list:
                videos_list = []

            for video in (response["items"]):
                videos_list.append(video["contentDetails"]["videoId"])

            return videos_list

        except:
            try:
                request = YOUTUBE.playlistItems().list(part="contentDetails", playlistId= playlist_link_id, maxResults = 50)
                response = request.execute()

                videos_list = get_next_page(response, YOUTUBE, playlist_link_id)
                if "Done" in videos_list:
                    videos_list = []

                for video in (response["items"]):
                    videos_list.append(video["contentDetails"]["videoId"])
                
                return videos_list

            except:
                return ["Invalid Playlist Id"]

def get_next_page(response:dict, YOUTUBE:build, playlist_id:str) -> List[str]:
    try:
        next_page_token = response["nextPageToken"]

        request = YOUTUBE.playlistItems().list(part="contentDetails", playlistId= playlist_id, pageToken = next_page_token, maxResults = 50)
        response = request.execute()

        videos_list: List[str] = []
        for video in (response["items"]):
            videos_list.append(video["contentDetails"]["videoId"])

        more = get_next_page(response, YOUTUBE,playlist_id)
        if more[0] != "Done":
            for video in more:
                videos_list.append(video)
        
        return videos_list

    except:
        return ["Done"]

def main():
    pass

if __name__ == "__main__":
    main()