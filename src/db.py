from os import mkdir, path, walk

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

import youtube as yt
from config import conf

DB_DIR = conf["DB_DIR"]
DATA_DIR = conf["DATA_DIR"]
VTT_DATA_DIR = conf["VTT_DATA_DIR"]
TXT_DATA_DIR = conf["TXT_DATA_DIR"]
PODCAST_YT_PLAYLIST_URL = conf["PODCAST_YT_PLAYLIST_URL"]
COLLECTION_NAME = "transcripts"

DATABASE = None
DOCS = None


def setup_data(force_update=False):
    global DOCS

    if DOCS is not None and not force_update:
        return DOCS

    for dir in [DATA_DIR, VTT_DATA_DIR, TXT_DATA_DIR]:
        if not path.exists(dir):
            mkdir(dir)

    videos_info = yt.get_videos_info_from_playlist(PODCAST_YT_PLAYLIST_URL)

    if "entries" not in videos_info or len(videos_info) == 0:
        print("Error getting video info. Exiting...")
        return

    id2title = {info["id"]: info["title"] for info in videos_info["entries"]}

    yt.download_all_transcripts(id2title)
    yt.convert_all_transcripts_to_txt(id2title)

    docs = []
    for _, _, filenames in walk(TXT_DATA_DIR):
        for file in filenames:
            try:
                loader = TextLoader(path.join(TXT_DATA_DIR, file), encoding="utf-8")
                docs.extend(loader.load_and_split())
            except Exception as e:
                print(e)
                pass

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(docs)

    DOCS = docs

    return docs

    # Debug prints
    # for id, title in id2title.items():
    #     print(f"ID: {id} | Title: {title}")
    #
    #
    # with open(txt_file_path, "r", encoding="utf-8") as txt_file:
    #     print("".join(txt_file.readlines()))


def init_db(
    embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
    collection_name=COLLECTION_NAME,
    db_dir=DB_DIR,
    force_update=False,
):
    global DATABASE

    if DATABASE is not None and not force_update:
        return DATABASE

    print("Initializing database")

    if path.exists(db_dir) and not force_update:
        print("Database exists on disk, using it")
        db = Chroma(
            embedding_function=embedding_function,
            persist_directory=db_dir,
            collection_name=collection_name,
        )
    else:
        if DOCS is None:
            setup_data()

        db = Chroma.from_documents(
            documents=DOCS,
            embedding_function=embedding_function,
            persist_directory=db_dir,
            collection_name=collection_name,
        )

    print("Database initialized")

    DATABASE = db


def search(query: str):
    if DATABASE is None:
        init_db()

    print(f"Searching database for query: '{query}'")

    docs = DATABASE.similarity_search(query, k=3)

    print(f"Successfully retrieved {len(docs)} documents")

    return [doc.page_content for doc in docs]
    # return docs


def test():
    while True:
        query = input("Enter query ('q' to quit): ")

        if query.lower() == "q":
            break

        docs = search(query)
        print(docs[0].page_content)
        print(f"Number of docs: {len(docs)}")


init_db()


if __name__ == "__main__":
    test()
