import re
from typing import Dict
from os import environ, mkdir, path, walk
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
import requests
from concurrent.futures import ThreadPoolExecutor

from config import conf

DATA_DIR = conf["DATA_DIR"]
VTT_DATA_DIR = conf["VTT_DATA_DIR"]
TXT_DATA_DIR = conf["TXT_DATA_DIR"]
YT_API_KEY = conf["YT_API_KEY"]


def get_videos_info_from_playlist(playlist_url):
    ydl_opts = {
        "quiet": True,  # Suppress console output
        "extract_flat": True,  # Extract videos as a flat list
        "force_generic_extractor": True,  # Use generic extractor for all sites
        "extractor_args": {
            "youtube": {"skip_download": True}
        },  # Skip downloading videos
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return info


def get_video_info(video_id: str):
    # transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # print(transcript)
    ydl_opts = {
        "quiet": True,
        "skip_download": True,  # Skip downloading the video
        "writesubtitles": True,  # Write subtitles to a file
        "writeautomaticsub": True,  # Write automatically generated subtitles
        "subtitleslangs": ["en"],  # Specify the language(s) of subtitles to extract
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)
        return info


def get_transript_url(video_info):
    return video_info.get("requested_subtitles", []).get("en", []).get("url", "")


def download_transcript(transcript_url: str, file_path: str, if_not_exists=False):
    if if_not_exists and path.exists(file_path):
        # Skip if transcript is already downloaded and flag is set
        return

    print(f"Downloading transcript to {file_path}")

    res = requests.get(transcript_url)
    if res.status_code != 200:
        print(f"Error: Unable to download file. Status code: {res.status_code}")
        return

    with open(file_path, "w") as file:
        for chunk in res.iter_content(chunk_size=8192):
            file.write(chunk.decode("utf-8"))
        # while True:
        #     chunk = res.content.read(8192)
        #     if not chunk:
        #         break
        #     file.write(chunk)
    print(f"File downloaded as {file_path}")


def download_all_transcripts(
    ids_to_titles: Dict[str, str], max_workers=8, if_not_exists=True
):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for id, title in ids_to_titles.items():
            video_info = get_video_info(id)
            url = get_transript_url(video_info)
            vtt_file_path = path.join(VTT_DATA_DIR, f"{id}.vtt")
            # download_transcript(url, vtt_file_path, if_not_exists=True)
            result = executor.submit(
                download_transcript, url, vtt_file_path, if_not_exists=if_not_exists
            )
            results.append(result)

    # Wait on all tasks to finish
    for res in results:
        res.result()


def vtt_to_text(vtt_file_path: str, txt_file_path: str, if_not_exists=False):
    if if_not_exists and path.exists(txt_file_path):
        # Skip if transcript is already converted to text and flag is set
        return

    lines: str
    with open(vtt_file_path, "r", encoding="utf-8") as vtt_file:
        lines = vtt_file.readlines()

    # Skip heading
    lines = lines[3:]

    i = 0
    text = ""
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if line == "" or re.match(r"^\d+:\d+:\d+", line):
            # Skip timestamp line
            continue

        # Merge lines until next line
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line == "":
                break
            line += f" {next_line}"
            i += 1

        if "<c>" in line:
            # Check if the line matches the VTT timestamp pattern
            # print(f"Skipping {line}")
            continue

        text += f"{line}\n"

    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        print(f"Converted vtt to txt as {txt_file_path}")
        txt_file.write(text)


def convert_all_transcripts_to_txt(
    ids_to_titles: Dict[str, str], max_workers=8, if_not_exists=True
):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for id, title in ids_to_titles.items():
            vtt_file_path = path.join(VTT_DATA_DIR, f"{id}.vtt")
            txt_file_path = path.join(TXT_DATA_DIR, f"transcript_{id}.txt")
            result = executor.submit(
                vtt_to_text, vtt_file_path, txt_file_path, if_not_exists=if_not_exists
            )
            results.append(result)

    # Wait on all tasks to finish
    for res in results:
        res.result()

