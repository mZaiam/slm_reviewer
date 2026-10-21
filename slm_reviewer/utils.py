import subprocess
import socket
import os
import atexit
import time

from dotenv import load_dotenv

from langchain_ollama import ChatOllama

load_dotenv()

def get_llm(model_name: str, num_ctx: int):
    """Loads a LLM model from the Oracle server.

    Args:
      model_name (str): the name of the model in .env.
      num_ctx (int): the number of context tokens.

    Returns:
      llm (ChatOllama): the loaded model.
    """
    model = str(os.getenv(model_name))
    llm = ChatOllama(model=model, base_url="http://localhost:11434", temperature=1.0, num_ctx=num_ctx)
    return llm

def ssh_tunnel():
    """Connects a SSH tunnel and ensures it closes when the script exits."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 11434)) != 0:
            print("[Network] Opening SSH tunnel to Oracle.")
            
            tunnel_process = subprocess.Popen(
                ["ssh", "-N", "-L", "11434:localhost:11434", "mzaiam"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            atexit.register(lambda: tunnel_process.terminate())
            
            for _ in range(5):
                if s.connect_ex(('127.0.0.1', 11434)) == 0:
                    print("[Network] Tunnel established.")
                    return
                time.sleep(1)
            print("[Network] Warning: Tunnel took too long to open.")
        else:
            print("[Network] Port 11434 is already open.")