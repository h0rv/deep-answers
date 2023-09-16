from hugchat import hugchat
from hugchat.login import Login
from time import sleep

import db
import prompt_utils
from config import conf

DATA_DIR = conf["DATA_DIR"]
HUGGINGFACE_EMAIL = conf["HUGGINGFACE_EMAIL"]
HUGGINGFACE_PASSWORD = conf["HUGGINGFACE_PASSWORD"]

MAX_TOKENS = 256
RETRIES = 3


chatbot = None


def login():
    # Log in to huggingface and grant authorization to huggingchat
    cookies = Login(HUGGINGFACE_EMAIL, HUGGINGFACE_PASSWORD).login()

    return cookies

    # Save cookies to the local directory
    # cookie_dir = f"{DATA_DIR}/cookies_snapshot"
    # sign.saveCookiesToDir(cookie_dir)

    # Load cookies when you restart your program:
    # sign = login(email, None)
    # cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.


def init_bot():
    print("Initializing chatbot...")
    global chatbot

    cookies = login()

    # Create a ChatBot
    chatbot = hugchat.ChatBot(
        cookies=cookies.get_dict()
    )  # or cookie_path="usercookies/<email>.json"

    # Switch to `meta-llama/Llama-2-70b-chat-hf`
    chatbot.switch_llm(1)

    # Create a new conversation
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)

    print("Chatbot initialized")


def prompt(input: str) -> str:
    if chatbot is None:
        init_bot()

    docs = db.search(input)
    docs = docs[:5]
    context = "\n\n".join(docs)

    print("Prompting model...")
    prompt_str = prompt_utils.get({"prompt": input, "context": context})
    print(prompt_str)

    output = "Failed to prompt model"
    for _ in range(RETRIES):
        try:
            output = chatbot.chat(text=prompt_str, max_new_tokens=MAX_TOKENS)
            break
        except Exception as e:
            print(e)
            sleep(0.5)

    print(f"Output: {output}")

    return output
