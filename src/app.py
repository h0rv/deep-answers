from os import environ, mkdir, path, walk
from typing import Dict

import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake
from transformers import pipeline

from config import conf

DATA_DIR = conf.DATA_DIR
VTT_DATA_DIR = conf.VTT_DATA_DIR
TXT_DATA_DIR = conf.TXT_DATA_DIR

# model = pipeline("question-answering", model="deepset/roberta-base-squad2")


# Get and set env vars
environ["HUGGINGFACEHUB_API_TOKEN"] = conf["HUGGINGFACEHUB_API_TOKEN"]


def setup_data():
    for dir in [DATA_DIR, VTT_DATA_DIR, TXT_DATA_DIR]:
        if not path.exists(dir):
            mkdir(dir)

    videos_info = get_yt_videos_info_from_playlist(PODCAST_YT_PLAYLIST_URL)

    if "entries" not in videos_info:
        print("Error getting video info. Exiting...")
        return

    id2title = {info["id"]: info["title"] for info in videos_info["entries"]}

    # download_all_transcripts(id2title)
    #
    # convert_all_transcripts_to_txt(id2title)

    docs = []
    for _, _, filenames in os.walk(TXT_DATA_DIR):
        for file in filenames:
            try: 
                loader = TextLoader(path.join(TXT_DATA_DIR, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e: 
                print(e)
                pass

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)

    # Debug prints
    # for id, title in id2title.items():
    #     print(f"ID: {id} | Title: {title}")
    #
    #
    # with open(txt_file_path, "r", encoding="utf-8") as txt_file:
    #     print("".join(txt_file.readlines()))


def main():
    setup_data()

    st.title("Get the answers about your Deep Questions")

    input = st.text_input("Enter question")
    # output = model(input)
    output = query_engine(input).print_response_stream()

    print(output)


if __name__ == "__main__":
    main()
