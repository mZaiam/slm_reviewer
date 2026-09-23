from langchain_core.messages import HumanMessage

from state import TopicState
from llm import get_llm

def draft_suggestion(state: TopicState, model_name: str, task: str):
    llm = get_llm(model_name=model_name)
    
    prompt = f"""
    You are managing a Quarto documentation project about {state["topic_name"]}.
    
    Here is the current index file:
    ---
    {state["index"]}
    ---
    
    Task: {task}
    """
    
    final_text = ""
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        print(chunk.content, end="", flush=True)
        final_text += chunk.content
    print()
        
    return {"suggestions": final_text}