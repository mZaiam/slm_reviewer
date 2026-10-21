def topic_suggestion_prompt(section: int) -> str:
    """Prompt for suggesting new topics for a given section.

    Args: 
      section (int): number of the section.
    
    Returns:
      prompt (str): the prompt.
    """
    prompt = f"""Given my current notes, suggest a new addition for the {section} section and its subsections. Only include the name of the topic, which needs to be a contribution to the current topics. Suggest only established and important methods for the field. In general, a topic represents a single article. Do not suggest topics that are already covered, or that do not add nothing to the current notes."""
    return prompt

def topic_review_prompt(section: int, topic_name: str) -> str:
    """Prompt for reviewing new suggestions.
    
    Args: 
      section (int): number of the section.
      topic_name (str): the name of the topic.
    
    Returns:
      prompt (str): the prompt.
    """
    prompt = f"""1. Remove any duplicate or highly similar concepts.
    2. Discard topics that do not fit into the section {section} of {topic_name}.
    3. Assign the remaining topics a sequential hierarchical number based on where they should fit in the section {section}. 
    Output strictly the final numbered list, which should include the previous topics of the section {section} alongside the new additions."""
    return prompt

def summary_prompt() -> str:
    prompt = """You are an expert AI researcher and academic writer. Your task is to synthesize the following technical documentation. Please provide a technical, concise summary structured exactly as follows:
    1. **Core Concept**: A brief explanation of the theory discussed.
    2. **Implementation Details**: An overview of the code provided, and how it is related to the theory presented.
    Keep the tone academic, precise, and direct. Do not include introductory fluff or conversational text."""
    return prompt