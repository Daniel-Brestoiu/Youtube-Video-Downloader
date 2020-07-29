import os
import subprocess
from pathlib import Path
from typing import List

"""
Control of youtube-dl
    - (youtube-dl) (-o for output)(output location) (-f for format) (format type)/(quality type) (url)
"""

def download_videos(unique_codes_list: List[str], path: str) -> None:
    """Given a list of unique video codes, downloads them all using the download_video(video_code, format = "mp4") function."""
    if path == "":
        path = Path.home()

    for x in unique_codes_list:
        assert type(x) == str, "Improper code."
        download_video(video_code=x, path = path)

def download_video(video_code: str, path: str = f"{Path.home()}", format: str = "mp4",) -> None:
    """
    Uses youtube-dl library to download a youtube video given the unique code for the youtube video.
    Default format type is mp4.
    :param video_code: The YouTube video ID you want to download
    """

    if path == "":
        path = Path.home()

    subprocess.run(["youtube-dl", "-o", f'{path}/%(title)s.%(ext)s', "-f", f"{format}/best", f"https://www.youtube.com/watch?v={video_code}"])

if __name__ == "__main__":
    download_video("")