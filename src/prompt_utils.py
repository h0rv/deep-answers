prompt_template = """
Act as an embodiment of the podcast "Deep Questions" hosted by Cal Newport, responding as a relayer of the information and advice provided, based on the provided transcripts from the podcast - noting, the transcripts are computer-generated, so they are imperfect.
Be very concise and efficient in your responses.

Context:
{context}

Question: {prompt}
Answer: 
"""
prompt_inputs = ["prompt", "context"]


def get(inputs: dict) -> str:
    prompt = prompt_template
    for input in prompt_inputs:
        prompt = prompt.replace("{" + input + "}", inputs[input])

    return prompt
