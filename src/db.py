import chromadb
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from config import conf

TXT_DATA_DIR = conf["TXT_DATA_DIR"]
DB_DIR = conf["DB_DIR"]
COLLECTION_NAME = "transcripts"


def load_transcripts():
    loader = DirectoryLoader(
        TXT_DATA_DIR, glob="**/*.txt", loader_cls=TextLoader, use_multithreading=True
    )
    docs = loader.load()
    return docs


def get_db(docs, embedding_function, collection_name=COLLECTION_NAME, db_dir=DB_DIR):
    db = Chroma.from_documents(
        docs,
        embedding_function,
        persist_directory=db_dir,
        collection_name=collection_name,
    )
    return db


def test():
    docs = load_transcripts()
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = get_db(docs, embedding_function)
    
    while True:
        query = input("Enter query ('q' to quit): ")

        if query.lower() == 'q': break

        docs = db.similarity_search(query)
        print(docs[0].page_content)

if __name__ == "__main__":
    test()
