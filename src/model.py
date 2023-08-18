from langchain import LLMChain, PromptTemplate
from langchain.llms import HuggingFaceHub

import db
from config import conf

# Get and set config variables
HUGGINGFACEHUB_API_TOKEN = conf["HUGGINGFACEHUB_API_TOKEN"]

# model = pipeline("question-answering", model="deepset/roberta-base-squad2")
model = HuggingFaceHub(
    # repo_id="bigscience/bloom-560m",
    # repo_id="google/flan-t5-base",
    repo_id="google/flan-t5-large",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    model_kwargs={  # https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        "min_length": 3,
        "max_length": 500,
        "temperature": 0.7,
        #     # "top_k": 50,
        #     # "top_p": 1.0,
        #     # "repetition_penalty": 1.1,
        #     # "early_stopping": True,
    },
)

prompt_template = """
Please write a response to the prompt, based on the provided context.
Note, the context provided are transcripts from a podcast called "Deep Questions" hosted by Cal Newport.
The transcripts are computer-generated, so they are imperfect.
{context}
Question: {prompt}
Answer: 
"""
prompt_inputs = ["prompt", "context"]

prompt = PromptTemplate(template=prompt_template, input_variables=prompt_inputs)

llm_chain = LLMChain(llm=model, prompt=prompt)


def prompt(prompt: str) -> str:
    docs = db.search(prompt)
    context = "\n\n".join(docs)
    print("Prompting model...")
    output = llm_chain.run({"prompt": prompt, "context": context})
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
