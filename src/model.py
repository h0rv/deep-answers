from os import mkdir, path, walk

from langchain import PromptTemplate, LLMChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import HuggingFaceHub

import youtube as yt

from config import conf

# Get and set config variables
HUGGINGFACEHUB_API_TOKEN = conf["HUGGINGFACEHUB_API_TOKEN"]
DATA_DIR = conf["DATA_DIR"]
VTT_DATA_DIR = conf["VTT_DATA_DIR"]
TXT_DATA_DIR = conf["TXT_DATA_DIR"]
PODCAST_YT_PLAYLIST_URL = conf["PODCAST_YT_PLAYLIST_URL"]


def setup_data():
    for dir in [DATA_DIR, VTT_DATA_DIR, TXT_DATA_DIR]:
        if not path.exists(dir):
            mkdir(dir)

    videos_info = yt.get_videos_info_from_playlist(PODCAST_YT_PLAYLIST_URL)

    if "entries" not in videos_info:
        print("Error getting video info. Exiting...")
        return

    id2title = {info["id"]: info["title"] for info in videos_info["entries"]}

    # download_all_transcripts(id2title)
    #
    # convert_all_transcripts_to_txt(id2title)

    docs = []
    for _, _, filenames in walk(TXT_DATA_DIR):
        for file in filenames:
            try:
                loader = TextLoader(path.join(TXT_DATA_DIR, file), encoding="utf-8")
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


setup_data()

# model = pipeline("question-answering", model="deepset/roberta-base-squad2")
model = HuggingFaceHub(
    repo_id="bigscience/bloom-560m",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    model_kwargs={
        # https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        "temperature": 0.6,
        "top_k": 50,
        "top_p": 1.0,
        "min_length": 3,
        "max_length": 250,
        "repetition_penalty": 1.1,
        # "early_stopping": True,
        },
)

prompt_template = """
Please write a response to the prompt, based on the provided context.
{context}
Question: {prompt}
Answer: 
"""
prompt_inputs = ["prompt", "context"]

prompt = PromptTemplate(template=prompt_template, input_variables=prompt_inputs)

llm_chain = LLMChain(prompt=prompt, llm=model)


def prompt(prompt: str, context="") -> str:
    output = llm_chain.run({"prompt": prompt, "context": context})
    print(output)
    return output
