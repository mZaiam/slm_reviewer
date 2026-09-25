from langchain_core.messages import HumanMessage

from state import TopicState
from utils import get_llm

def draft_suggestion(state: TopicState, model_name: str, task: str):
    """Drafts a suggestion for the topic."""
    llm = get_llm(model_name=model_name)
    
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
    
    return {
        "suggestions": updated_suggestions,
        "suggestions_count": state.get("suggestions_count", 0) + 1
    }