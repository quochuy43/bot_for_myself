from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

_embeddings = None

def get_retriever(collection_name="about_myself", k=3):
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
        )

    client = MongoClient(os.getenv("MONGO_ATLAS"))
    db = client["vector_store"]
    collection = db[collection_name]

    vectordb = MongoDBAtlasVectorSearch(
        embedding=_embeddings,
        collection=collection,
        index_name="vector_index",
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    return retriever