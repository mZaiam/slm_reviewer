from functools import partial
from langgraph.graph import StateGraph, START, END

from state import TopicState
from nodes.files import load_topic, save_suggestion, should_continue, save_topics, remove_file
from nodes.drafts import draft_suggestion, review_topics

def topic_suggestion_workflow(
    model: str, 
    num_ctx: int, 
    n: int,
    task_suggestion: str, 
    task_review: str, 
    save_fig_path: str = "images/topic_suggestion_workflow.png"
):
    workflow = StateGraph(TopicState)

    workflow.add_node("load_topic", load_topic)
    workflow.add_node("draft_suggestion", partial(draft_suggestion, model_name=model, num_ctx=num_ctx, task=task_suggestion))
    workflow.add_node("save_suggestion", save_suggestion)
    workflow.add_node("review_topics", partial(review_topics, model_name=model, num_ctx=num_ctx, task=task_review))
    workflow.add_node("save_topics", save_topics)
    workflow.add_node("remove_file", remove_file)

    workflow.add_edge(START, "load_topic")
    workflow.add_edge("load_topic", "draft_suggestion")
    workflow.add_conditional_edges(
        "draft_suggestion", 
        lambda state: should_continue(state, n=n),
        {"continue": "draft_suggestion", "end": "save_suggestion"}
    )
    workflow.add_edge("save_suggestion", "review_topics")
    workflow.add_edge("review_topics", "save_topics")
    workflow.add_edge("save_topics", "remove_file")
    workflow.add_edge("remove_file", END)

    app = workflow.compile()

    if save_fig_path:
        try:
            graph_image_data = app.get_graph().draw_mermaid_png()
            with open(save_fig_path, "wb") as f:
                f.write(graph_image_data)
        except Exception as e:
            print(f"[Warning] Could not save graph figure: {e}")

    return app