import os
import pickle
from langchain_community.retrievers import TFIDFRetriever
from rag_for_me.build.loader.document_loader import split_markdown_by_heading

CACHE_DIR = os.path.join("rag_for_me", "cache")
CACHE_PATH = os.path.join(CACHE_DIR, "keyword_retriever.pkl")

def get_keyword_retriever(force_reload: bool = False) -> TFIDFRetriever:
    """
    Returns keyword retriever from cache (if present), or creates new one if not cached or force_reload = True.
    """

    if not force_reload and os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)

    docs = split_markdown_by_heading()
    retriever = TFIDFRetriever.from_documents(docs)

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(retriever, f)

    return retriever
