import os

"""
Control of youtube-dl
    - youtube-dl -o '/Users/daniel/Desktop/Music/%(title)s.%(ext)s' -f mp4/best 'https://www.youtube.com/watch?v=Djsi8qcVelo'
    - (youtube-dl) (-o for output)(output location) (-f for format) (format type)/(quality type) (url)
"""



def download_videos(unique_codes_list):
    """Given a list of unique video codes, downloads them all using the download_video(video_code, format = "mp4") function."""
    for x in unique_codes_list:
        download_video(video_code = str(x))

def download_video(video_code, format = "mp4"):
    """Uses youtube-dl library to download a youtube video given the unique code for the youtube video.
    Default format type is mp4."""

    command = "youtube-dl -o '/Users/daniel/Desktop/Music/%(title)s.%(ext)s' -f {}/best 'https://www.youtube.com/watch?v={}'".format(str(format),str(video_code))
    os.system(command)


if __name__ == "__main__":
    pass

