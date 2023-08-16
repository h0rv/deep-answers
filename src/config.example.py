from os import path

DATA_DIR = "data"

conf = {
    "HUGGINGFACEHUB_API_TOKEN": "",
    "YT_API_KEY": "",
    "PODCAST_YT_PLAYLIST_URL": "https://www.youtube.com/playlist?list=PL8xK8kBHHUX4NW8GqUsyFhBF_xCnzIdPe",
    "DATA_DIR": DATA_DIR,
    "VTT_DATA_DIR": path.join(DATA_DIR, "vtts"),
    "TXT_DATA_DIR": path.join(DATA_DIR, "txt"),
    "DB_DIR": path.join(DATA_DIR, "db"),
}
