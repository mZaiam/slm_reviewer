import os
from dotenv import load_dotenv
from smolagents import OpenAIModel, CodeAgent

from tools import read_file, write_correction
from utils import ssh_tunnel

ssh_tunnel()
load_dotenv()

MODEL = str(os.getenv("QWEN354B"))

model = OpenAIModel(
    model_id=MODEL,
    api_base="http://localhost:11434/v1",
    api_key="ollama",
)

agent = CodeAgent(
    tools=[read_file],
    model=model
)

QUARTO_DIR = os.getenv("QUARTO_DIR")

local_file = str(QUARTO_DIR) + "diffusion_models/index.qmd"
agent.run(f"Read the file at {local_file} using read_file. Summarize it. Do not perform any other actions.")