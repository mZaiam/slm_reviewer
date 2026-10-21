import os
import glob
import re
import json
from dotenv import load_dotenv

import frontmatter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from slm_reviewer.utils import ssh_tunnel

def resolve_quarto_embeds(raw_content: str, qmd_file_path: str) -> str:
    """Finds Quarto embed tags and replaces them with the Jupyter Notebook code.
    
    Args:
      raw_content (str): the raw content in the .qmd.
      qmd_file_path (str): the path of the .qmd.

    Returns:
      final_text (str): the final text with the .ipynb code. 
    """
    pattern = r"\{\{<\s*embed\s+([^\s>]+)\s*>\}\}"
    
    def replace_match(match):
        embed_path = match.group(1)
        ipynb_path = os.path.normpath(os.path.join(os.path.dirname(qmd_file_path), embed_path))
        
        try:
            with open(ipynb_path, 'r', encoding='utf-8') as nb_file:
                notebook = json.load(nb_file)
            
            code_cells = []
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    source = "".join(cell.get("source", []))
                    if source.strip():
                        code_cells.append(source)
                        
            combined_code = "\n\n".join(code_cells)
            return f"\n### Implementation\n```python\n{combined_code}\n```\n"
            
        except Exception as e:
            print(f"  [Warning] Could not load embedded notebook {ipynb_path}: {e}")
            return f"\n[Code from {embed_path} missing]\n"

    final_text = re.sub(pattern, replace_match, raw_content)
    return final_text

def build_db():
    load_dotenv()
    ssh_tunnel()

    QUARTO_DIR = os.getenv("QUARTO_DIR", "./")
    MODEL = os.getenv("GEMMAEMBEDDING2")

    embeddings = OllamaEmbeddings(
        model=MODEL,
        base_url="http://localhost:11434"
    )

    headers_to_split_on = [
        ("##", "Section"),
        ("###", "Subsection"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    all_chunks = []

    qmd_files = glob.glob(os.path.join(QUARTO_DIR, "**/*.qmd"), recursive=True)

    print(f"Found {len(qmd_files)} .qmd files...")

    for file_path in qmd_files:
        if os.path.basename(file_path).lower() == "index.qmd":
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                
                doc_title = post.metadata.get("title", os.path.basename(file_path))

                resolved_content = resolve_quarto_embeds(post.content, file_path)
                
                file_chunks = markdown_splitter.split_text(resolved_content)
                
                for chunk in file_chunks:
                    formatted_text = f"title: {doc_title} | text: {chunk.page_content}"
                    chunk.page_content = formatted_text
                    
                    chunk.metadata["source"] = file_path
                    chunk.metadata["title"] = doc_title
                    
                    all_chunks.append(chunk)
                    
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Total of {len(all_chunks)} chunks generated.")

    vector_db_path = "./chroma_db"

    print("Generating vectors and saving to disk...")
    vector_store = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=vector_db_path
    )
    print(f"Vector database saved to {vector_db_path}")

if __name__ == "__main__":
    load_dotenv()
    build_db()