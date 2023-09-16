from langchain import LLMChain, PromptTemplate
from langchain.llms import HuggingFaceHub

import db
import prompt_utils
from config import conf

# Get and set config variables
HUGGINGFACEHUB_API_TOKEN = conf["HUGGINGFACEHUB_API_TOKEN"]

# model = pipeline("question-answering", model="deepset/roberta-base-squad2")
model = HuggingFaceHub(
    # repo_id="bigscience/bloom-560m",
    # repo_id="google/flan-t5-base",
    # repo_id="google/flan-t5-large",
    repo_id="stabilityai/stablecode-completion-alpha-3b-4k",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    model_kwargs={  # https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        "min_length": 3,
        "max_length": 100,
        "temperature": 0.7,
        #     # "top_k": 50,
        #     # "top_p": 1.0,
        #     # "repetition_penalty": 1.1,
        #     # "early_stopping": True,
    },
)

llm_chain = None


def prompt(input: str) -> str:
    if not llm_chain:
        llm_chain = LLMChain(llm=model)

    docs = db.search(input)
    context = "\n\n".join(docs)

    print("Prompting model...")
    prompt_str = prompt_utils.get({"prompt": input, "context": context})

    output = llm_chain.run(prompt_str)
    print(f"Output: {output}")

    return output


def test():
    while True:
        query = input("Enter query ('q' to quit): ")

        if query.lower() == "q":
            break

        prompt(query)


if __name__ == "__main__":
    test()
