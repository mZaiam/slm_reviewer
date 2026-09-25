import subprocess
import socket
import os

from dotenv import load_dotenv

from langchain_ollama import ChatOllama

load_dotenv()

def get_llm(model_name="QWEN354B"):
    """Loads a LLM model from the Oracle server.

    Args:
      model_name (str): the name of the model in .env.

    Returns:
      llm (ChatOllama): the loaded model.
    """
    model = str(os.getenv(model_name))
    llm = ChatOllama(model=model, base_url="http://localhost:11434", temperature=1.0)
    return llm

def ssh_tunnel():
    """Connects a SSH tunnel to the Oracle server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 11434)) != 0:
            subprocess.run(["ssh", "-f", "-N", "mzaiam"])