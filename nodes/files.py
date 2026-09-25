import os
import glob

from state import TopicState

def load_topic(state: TopicState):
    """Loads the index.qmd and the file paths from the topic."""
    index_path = os.path.join(state["topic_dir"], "index.qmd")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
        
    search_pattern = os.path.join(state["topic_dir"], "**", "*.qmd")
    qmd_files = glob.glob(search_pattern, recursive=True)
    
    file_names = [
        os.path.relpath(f, state["topic_dir"]) 
        for f in qmd_files 
        if not f.endswith("index.qmd")
    ]
    
    return {
        "index": index_content,
        "files": file_names
    }

def save_suggestion(state: TopicState):
    """Saves the suggestion of the LLM into a file."""
    with open(state["suggestions_path"], "a", encoding="utf-8") as f:
        f.write(state["suggestions"].strip() + "\n")
    return {}

def should_continue(state: TopicState, n: int) -> str:
    """Checks if the number of suggestions has been achieved."""
    if state.get("suggestions_count", 0) < n:
        return "continue"
    return "end"