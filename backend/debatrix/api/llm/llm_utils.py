import ollama
from pathlib import Path

def create_llm_model(name: str, modelfile: str):
    # load generator modelfile

    ollama.create(model=name, modelfile=modelfile)
    return name

def get_llm_response(model, prompt, context = []):
    response = ollama.generate(
        model=model, 
        prompt=prompt,
        context=context
    )
    return response["response"]

def summarise(txt):
    response = get_llm_response("summarise", txt)
    points = response.split('\n')
    return points

def fact_check(txt):
    response = get_llm_response("factcheck", txt)
    return response