import os
from functools import partial
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END

from slm_reviewer.state import SummaryState
from slm_reviewer.prompts import summary_prompt
from slm_reviewer.nodes.files import load_qmd, save_synthesis
from slm_reviewer.nodes.drafts import synthesize_document
from slm_reviewer.utils import ssh_tunnel

def summary_workflow(
    file_path: str, 
    output_path: str, 
    model_name: str, 
    num_ctx: int,
    save_fig_path: str = "images/summary_workflow.png"
) -> SummaryState:
    """Summary workflow.

    Args:
      file_path (str): path of the file.
      output_path (str): output path of the summary.
      model (str): name of the model. 
      num_ctx (int): context window.
    """
    load_dotenv()
    ssh_tunnel()

    QUARTO_DIR = os.getenv("QUARTO_DIR")
    SUMMARIZE_PROMPT = summary_prompt()

    workflow = StateGraph(SummaryState)
    
    workflow.add_node("load_qmd", load_qmd)
    workflow.add_node("synthesize_document", partial(
        synthesize_document, 
        model_name=model_name, 
        num_ctx=num_ctx, 
        prompt=SUMMARIZE_PROMPT
    ))
    workflow.add_node("save_synthesis", save_synthesis)
    
    workflow.add_edge(START, "load_qmd")
    workflow.add_edge("load_qmd", "synthesize_document")
    workflow.add_edge("synthesize_document", "save_synthesis")
    workflow.add_edge("save_synthesis", END)
    
    app = workflow.compile()

    if save_fig_path:
        try:
            graph_image_data = app.get_graph().draw_mermaid_png()
            with open(save_fig_path, "wb") as f:
                f.write(graph_image_data)
        except Exception as e:
            print(f"[Warning] Could not save graph figure: {e}")
    
    absolute_file_path = os.path.join(QUARTO_DIR, file_path)
    
    initial_state = {
        "file_path": absolute_file_path,
        "output_path": output_path,
        "raw_content": "",
        "summary": ""
    }
    
    final_state = app.invoke(initial_state)
    
    print("\n--- Workflow Complete ---")
    print(f"Summary saved to: {output_path}")
    
    return final_state