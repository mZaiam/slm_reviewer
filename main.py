import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from utils import ssh_tunnel

ssh_tunnel()
load_dotenv()

MODEL = str(os.getenv("QWEN257B"))

llm = ChatOllama(
    model=MODEL,
    base_url="http://localhost:11434"
)

class ReviewerState(TypedDict):
    diffusion_file_path: str
    topics_file_path: str
    suggestions_file_path: str
    current_notes: str
    new_topics: str
    final_plan: str

def load_files(state: ReviewerState):
    """Python reads the local files into the state memory."""
    print("Node 1: Reading Quarto files...")
    with open(state["diffusion_file_path"], "r", encoding="utf-8") as f:
        notes = f.read()
    with open(state["topics_file_path"], "r", encoding="utf-8") as f:
        topics = f.read()
    
    return {"current_notes": notes, "new_topics": topics}

def draft_plan(state: ReviewerState):
    """The LLM analyzes the text and drafts the plan."""
    print("Node 2: LLM is synthesizing the integration plan...")
    
    prompt = f"""
    Here are my current diffusion-model topics:
    ---
    {state["current_notes"]}
    ---

    Here are the new topics to add:
    ---
    {state["new_topics"]}
    ---

    Identify how the new topics should be integrated into my current notes. The additions should be listed according to my current numbering system (e.g., 4. New Topic, 4.1. New Subtopic). List topics only by name, do not explain them.
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        print(chunk.content, end="", flush=True)
        final_text += chunk.content
        
    print("\n\nFinished streaming.")
    return {"final_plan": final_text}

def save_plan(state: ReviewerState):
    """Python saves the final draft to the disk."""
    print("Node 3: Saving the final plan to disk...")
    with open(state["suggestions_file_path"], "w", encoding="utf-8") as f:
        f.write(state["final_plan"])
    
    return {}

workflow = StateGraph(ReviewerState)

workflow.add_node("load_files", load_files)
workflow.add_node("draft_plan", draft_plan)
workflow.add_node("save_plan", save_plan)

workflow.add_edge(START, "load_files")
workflow.add_edge("load_files", "draft_plan")
workflow.add_edge("draft_plan", "save_plan")
workflow.add_edge("save_plan", END)

reviewer_graph = workflow.compile()

QUARTO_DIR = os.getenv("QUARTO_DIR")

initial_state = {
    "diffusion_file_path": os.path.join(QUARTO_DIR, "diffusion_models", "index.qmd"),
    "topics_file_path": os.path.join(QUARTO_DIR, "_agent", "topics.md"),
    "suggestions_file_path": os.path.join(QUARTO_DIR, "_agent", "dms_future_topics.md"),
    "current_notes": "",
    "new_topics": "",
    "final_plan": ""
}

print("\nStarting the Reviewer Pipeline...")
result = reviewer_graph.invoke(initial_state)

print("\nPipeline Complete!")
print(f"Plan saved to: {result['suggestions_file_path']}")