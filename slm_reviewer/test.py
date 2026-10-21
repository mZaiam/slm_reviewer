import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from utils import ssh_tunnel

ssh_tunnel()
load_dotenv()

MODEL = os.getenv("GEMMAEMBEDDING2")

embeddings = OllamaEmbeddings(
    model=MODEL,
    base_url="http://localhost:11434"
)

vector_db_path = "./chroma_db"

vector_store = Chroma(
    persist_directory=vector_db_path,
    embedding_function=embeddings
)

query = "Implementation of DPS"

print(f"Searching for: '{query}'\n")

results = vector_store.similarity_search_with_score(query, k=3)

print("-" * 50)
for i, (doc, score) in enumerate(results, 1):
    print(f"Result {i} | Distance: {score:.4f}")
    print(f"Origin: {doc.metadata.get('title', 'Unknown')}")
    print(f"Path: {doc.metadata.get('source', 'Unknown')}")
    print("\nRetrieved chunk:")
    print(doc.page_content) 
    print("-" * 50)