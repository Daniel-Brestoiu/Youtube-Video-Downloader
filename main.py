import googleapiclient
from googleapiclient.discovery import build

API_key = 'AIzaSyBs1qMkQYzS4Vr2oCBYHOfx_TTcM6xYGUk'

youtube = build("youtube", "v3", developerKey= API_key)

request = youtube.search().list(q= "Music", part = "snippet", type = "video")      #type --> googleapiclient.http.HttpRequest
result = request.execute()

print()
for item in result["items"]:
    print(item['snippet']["title"])
    print()