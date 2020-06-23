import googleapiclient
from googleapiclient.discovery import build

API_key = 'AIzaSyBs1qMkQYzS4Vr2oCBYHOfx_TTcM6xYGUk'

youtube = build("youtube", "v3", developerKey= API_key)


"""
query = 'music'
request = youtube.search().list(q= str(query), part = "snippet", type = "video")      #type --> googleapiclient.http.HttpRequest
result = request.execute()


print()
for item in result["items"]:
    print(item['snippet']["title"], "\n", item["id"]["videoId"])
    print()
"""


playlist = youtube.playlistItems().list(part = "contentDetails",  playlistId = "PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG").execute()

videos_list = []
for video in (playlist["items"]):
    videos_list.append(video["contentDetails"]["videoId"])

print(videos_list)



#To find a video, https://www.youtube.com/watch?v=(videoId)
#Channel UCrS7pF40yRheVTFXzuawvwA
#Playlist PL4y8ZuWSzyRRTt3i-XujOg7NYX72XV8MG
