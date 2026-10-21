import os
import glob
import timeit
import frontmatter

from slm_reviewer.state import TopicState, SummaryState

def load_topic(state: TopicState):
    """Loads the index.qmd and the file paths from the topic.
    
    Args:
      state (str): the state object.
    """
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
    """Saves the suggestion of the LLM into a file.
    
    Args:
      state (str): the state object.
    """
    s = timeit.default_timer()
    with open(state["suggestions_path"], "a", encoding="utf-8") as f:
        f.write(state["suggestions"].strip() + "\n")
    e = timeit.default_timer()
    print(f"[Node] save_suggestion ({(e - s):.2f} s)")
    return {}

def should_continue(state: TopicState, n: int) -> str:
    """Checks if the number of suggestions has been achieved.
    
    Args:
      state (str): the state object.
      n (int): the number of desired suggestions.
    
    Returns:
      decision (str): the decision to continue or not.
    """

    s = timeit.default_timer()
    e = timeit.default_timer()
    print(f"[Node] should_continue ({(e - s):.2f} s)")

    if state.get("suggestions_count", 0) < n:
        decision = "continue"
        return decision
    decision = "end"
    return decision

def save_topics(state: TopicState):
    """Saves the final, numbered list to disk.
    
    Args:
      state (str): the state object.
    """
    s = timeit.default_timer()
    final_path = state["suggestions_path"].replace(".md", "_final.md")
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(state["final_suggestions"] + "\n")
    e = timeit.default_timer()
    print(f"[Node] save_topics ({(e - s):.2f} s)")
    return {}

def remove_file(state: TopicState):
    """Deletes the temporary raw suggestions file from the disk.
    
    Args:
      state (str): the state object.
    """
    s = timeit.default_timer()
    path = state["suggestions_path"]
    
    if os.path.exists(path):
        os.remove(path)
        
    e = timeit.default_timer()
    print(f"[Node] remove_file ({(e - s):.2f} s)")
    
    return {"suggestions": ""}

def load_qmd(state: SummaryState):
    """Loads a single .qmd file and extracts its frontmatter and content.
    
    Args:
      state (SummaryState): the state object.
    """
    s = timeit.default_timer()
    
    with open(state["file_path"], "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        title = post.metadata.get("title", os.path.basename(state["file_path"]))
        content = f"Title: {title}\n\n{post.content}"
        
    e = timeit.default_timer()
    print(f"[Node] load_qmd ({(e - s):.2f} s)")
    
    return {"raw_content": content}

def save_synthesis(state: SummaryState):
    """Saves the generated summary to the designated output path.
    
    Args:
      state (SummaryState): the state object.
    """
    s = timeit.default_timer()
    
    with open(state["output_path"], "w", encoding="utf-8") as f:
        f.write(state["summary"].strip() + "\n")
        
    e = timeit.default_timer()
    print(f"[Node] save_synthesis ({(e - s):.2f} s)")
    
    return {}