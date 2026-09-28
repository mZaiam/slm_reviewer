import os
import glob
import timeit

from state import TopicState

def load_topic(state: TopicState):
    """Loads the index.qmd and the file paths from the topic."""
    s = timeit.default_timer()
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

    e = timeit.default_timer()
    print(f"[Node] load_topic ({(e - s):.2f} s)")
    
    return {
        "index": index_content,
        "files": file_names
    }

def save_suggestion(state: TopicState):
    """Saves the suggestion of the LLM into a file."""
    s = timeit.default_timer()
    with open(state["suggestions_path"], "a", encoding="utf-8") as f:
        f.write(state["suggestions"].strip() + "\n")
    e = timeit.default_timer()
    print(f"[Node] save_suggestion ({(e - s):.2f} s)")
    return {}

def should_continue(state: TopicState, n: int) -> str:
    """Checks if the number of suggestions has been achieved."""

    s = timeit.default_timer()
    e = timeit.default_timer()
    print(f"[Node] should_continue ({(e - s):.2f} s)")

    if state.get("suggestions_count", 0) < n:
        return "continue"
    return "end"

def save_topics(state: TopicState):
    """Saves the final, numbered list to disk."""
    s = timeit.default_timer()
    final_path = state["suggestions_path"].replace(".md", "_final.md")
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(state["final_suggestions"] + "\n")
    e = timeit.default_timer()
    print(f"[Node] save_topics ({(e - s):.2f} s)")
    return {}


def remove_file(state: TopicState):
    """Deletes the temporary raw suggestions file from the disk."""
    s = timeit.default_timer()
    path = state["suggestions_path"]
    
    if os.path.exists(path):
        os.remove(path)
        
    e = timeit.default_timer()
    print(f"[Node] remove_file ({(e - s):.2f} s)")
    
    return {"suggestions": ""}