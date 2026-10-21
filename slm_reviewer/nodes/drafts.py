import timeit

from langchain_core.messages import HumanMessage

from state import TopicState
from utils import get_llm

def draft_suggestion(state: TopicState, model_name: str, num_ctx: int, task: str):
    """Drafts a suggestion for the topic."""
    s = timeit.default_timer()
    llm = get_llm(model_name=model_name, num_ctx=num_ctx)
    
    prompt = f"""
    You are managing a Quarto documentation project about {state["topic_name"]}.
    
    Here is the current index file:
    ---
    {state["index"]}
    ---
    
    Task: {task}

    Do not repeat these:
    {state['suggestions']}
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        print(chunk.content, end="", flush=True)
        final_text += chunk.content
    print()
        
    new_suggestion = final_text.strip()
    
    current_suggestions = state.get("suggestions", "")
    updated_suggestions = current_suggestions + "\n" + new_suggestion

    e = timeit.default_timer()
    print(f"[Node] draft_suggestion ({(e - s):.2f} s)")
    
    return {
        "suggestions": updated_suggestions,
        "suggestions_count": state.get("suggestions_count", 0) + 1
    }

def review_topics(state: TopicState, model_name: str, num_ctx: int, task: str):
    """Filters, deduplicates, and numbers the raw suggestions."""
    s = timeit.default_timer()
    llm = get_llm(model_name=model_name, num_ctx=num_ctx)
    
    prompt = f"""
    You are an expert editor for a theoretical documentation project on {state['topic_name']}.
    
    Here is the current index file:
    ---
    {state['index']}
    ---
    
    Here is a raw list of brainstormed topics:
    ---
    {state['suggestions']}
    ---
    
    Task:
    {task}
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        print(chunk.content, end="", flush=True)
        final_text += chunk.content
    print()

    e = timeit.default_timer()
    print(f"[Node] review_topics ({(e - s):.2f} s)")
        
    return {"final_suggestions": final_text.strip()}