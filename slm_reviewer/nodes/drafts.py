import timeit

from langchain_core.messages import HumanMessage

from slm_reviewer.state import TopicState, SummaryState
from slm_reviewer.utils import get_llm

def draft_suggestion(state: TopicState, model_name: str, num_ctx: int, prompt: str):
    """Drafts a suggestion for the topic.
    
    Args:
      state (TopicState): the state object.
      model_name (str): the name of the model in .env.
      num_ctx (int): the number of context tokens.
      prompt (str): the task prompt. 
    """
    s = timeit.default_timer()
    llm = get_llm(model_name=model_name, num_ctx=num_ctx)
    
    full_prompt = f"""
    You are managing a Quarto documentation project about {state["topic_name"]}.
    
    Here is the current index file:
    ---
    {state["index"]}
    ---
    
    Task: {prompt}

    Do not repeat these:
    {state['suggestions']}
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=full_prompt)]):
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

def review_topics(state: TopicState, model_name: str, num_ctx: int, prompt: str):
    """Filters, deduplicates, and numbers the raw suggestions.
    
    Args:
      state (TopicState): the state object.
      model_name (str): the name of the model in .env.
      num_ctx (int): the number of context tokens.
      prompt (str): the task prompt. 
    """
    s = timeit.default_timer()
    llm = get_llm(model_name=model_name, num_ctx=num_ctx)
    
    full_prompt = f"""
    You are an expert editor for a theoretical documentation project on {state['topic_name']}.
    
    Here is the current index file:
    ---
    {state['index']}
    ---
    
    Here is a raw list of brainstormed topics:
    ---
    {state['suggestions']}
    ---
    
    Task: {prompt}
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=full_prompt)]):
        print(chunk.content, end="", flush=True)
        final_text += chunk.content
    print()

    e = timeit.default_timer()
    print(f"[Node] review_topics ({(e - s):.2f} s)")
        
    return {"final_suggestions": final_text.strip()}

def synthesize_document(state: SummaryState, model_name: str, num_ctx: int, prompt: str):
    """Synthesizes the content of a .qmd file.
    
    Args:
      state (SynthesisState): the state object.
      model_name (str): the name of the model in .env.
      num_ctx (int): the number of context tokens.
      prompt (str): the task prompt. 
    """
    s = timeit.default_timer()
    llm = get_llm(model_name=model_name, num_ctx=num_ctx)
    
    full_prompt = f"""
    {prompt}
    
    Document:
    ---
    {state['raw_content']}
    ---
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=full_prompt)]):
        print(chunk.content, end="", flush=True)
        final_text += chunk.content
    print()

    e = timeit.default_timer()
    print(f"[Node] synthesize_document ({(e - s):.2f} s)")
        
    return {"summary": final_text.strip()}