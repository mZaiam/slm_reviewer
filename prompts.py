def topic_suggestion_prompt(section: int) -> str:
    return f"""Given my current notes, suggest a new addition for the {section} section and its subsections. Only include the name of the topic, which needs to be a contribution to the current topics. Suggest only established and important methods for the field. In general, a topic represents a single article. Do not suggest topics that are already covered, or that do not add nothing to the current notes. The return format should follow: METHOD NAME (METHOD ACRONYM)."""

def topic_review_prompt(section: int, topic_name: str) -> str:
    return f"""1. Remove any duplicate or highly similar concepts.
2. Discard topics that do not fit into the section {section} of {topic_name}.
3. Assign the remaining topics a sequential hierarchical number based on where they should fit in the section {section}. 
Output strictly the final numbered list, which should include the previous topics of the section alongside the new additions."""