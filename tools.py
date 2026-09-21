import os
from smolagents import tool

@tool
def read_file(path: str) -> str:
    """Reads the content of a text file.

    Args:
      path: The complete path to the file.
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_correction(original_path: str, corrected_content: str) -> str:
    """Saves the corrected text to a new file.
    
    Args:
      original_path: The path of the file that was read.
      corrected_content: The full text with grammar and flow corrections.
    """
    try:
        base, ext = os.path.splitext(original_path)
        safe_path = f"{base}_corrected{ext}"
        
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(corrected_content)
        return f"Saved corrected file to {safe_path}"
    except Exception as e:
        return f"Error writing file: {e}"