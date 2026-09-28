import os
from dotenv import load_dotenv

from prompts import topic_suggestion_prompt, topic_review_prompt
from workflows.suggestion import topic_suggestion_workflow
from utils import ssh_tunnel

ssh_tunnel()
load_dotenv()

QUARTO_DIR = os.getenv("QUARTO_DIR")
MODEL = "GEMMA4E4B"
NUM_CTX = 1024

TOPIC_NAME = "diffusion_models"
TOPIC_DIR = os.path.join(QUARTO_DIR, TOPIC_NAME)
SUGGESTIONS_PATH = os.path.join(QUARTO_DIR, "_agent", f"{TOPIC_NAME}_suggestions.md")

N_SUGGESTIONS = 5
SECTION = 1

TASK_SUGGESTION = topic_suggestion_prompt(SECTION)
TASK_REVIEW = topic_review_prompt(SECTION, TOPIC_NAME)

app = topic_suggestion_workflow(
    model=MODEL, 
    num_ctx=NUM_CTX, 
    n=N_SUGGESTIONS, 
    task_suggestion=TASK_SUGGESTION, 
    task_review=TASK_REVIEW
)

initial_state = {
    "topic_name": TOPIC_NAME,
    "topic_dir": TOPIC_DIR,
    "index": "",
    "files": [],
    "suggestions_path": SUGGESTIONS_PATH,
    "suggestions": "",
    "suggestions_count": 0,
    "final_suggestions": ""
}

final_state = app.invoke(initial_state)