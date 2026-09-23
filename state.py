from typing import TypedDict, List

class TopicState(TypedDict):
    topic_name: str
    topic_dir: str

    index: str
    files: List[str]

    suggestions_dir: str
    suggestions: str