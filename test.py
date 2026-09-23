import os
from functools import partial
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END

from state import TopicState
from nodes.files import load_topic, save_suggestion
from nodes.drafts import draft_suggestion
from utils import ssh_tunnel

ssh_tunnel()
load_dotenv()

QUARTO_DIR = os.getenv("QUARTO_DIR")
MODEL = "QWEN257B"

TASK = """Given my current notes, suggest a new addition for the 1. Theoretical Foundation section. Only include the name of the topic, which needs to be a contribution to the current topics. Suggest only established and important methods for the field. Do not suggest topics that are already covered, or that do not add nothing to the current notes. The return format should follow: METHOD NAME (METHOD ACRONYM).
"""

topic_name = "diffusion_models"
topic_dir = os.path.join(QUARTO_DIR, topic_name)
suggestions_dir = os.path.join(QUARTO_DIR, "_agent", f"{topic_name}_suggestions.md")

initial_state: TopicState = {
    "topic_name": topic_name,
    "topic_dir": topic_dir,
    "index": "",
    "files": [],
    "suggestions_dir": suggestions_dir,
    "suggestions": ""
}

workflow = StateGraph(TopicState)

workflow.add_node("load_topic", load_topic)
workflow.add_node("draft_suggestion", partial(draft_suggestion, model_name=MODEL, task=TASK))
workflow.add_node("save_suggestion", save_suggestion)

workflow.add_edge(START, "load_topic")
workflow.add_edge("load_topic", "draft_suggestion")
workflow.add_edge("draft_suggestion", "save_suggestion")
workflow.add_edge("save_suggestion", END)

app = workflow.compile()
final_state = app.invoke(initial_state)