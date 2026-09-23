import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

def get_llm(model_name="QWEN354B"):
    model = str(os.getenv(model_name))
    return ChatOllama(
        model=model,
        base_url="http://localhost:11434"
    )