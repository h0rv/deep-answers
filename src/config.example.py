from os import path

conf = {
    "HUGGINGFACEHUB_API_TOKEN": "",
    "YT_API_KEY": "",
    "PODCAST_YT_PLAYLIST_URL": "https://www.youtube.com/playlist?list=PL8xK8kBHHUX4NW8GqUsyFhBF_xCnzIdPe",
    "DATA_DIR": "data",
}
conf += {
    "VTT_DATA_DIR": path.join(conf["DATA_DIR"], "vtts"),
    "TXT_DATA_DIR": path.join(conf["DATA_DIR"], "txt"),
    "DB_DIR": path.join(conf["DATA_DIR"], "db"),
}
