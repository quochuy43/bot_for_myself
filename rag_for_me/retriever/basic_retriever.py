from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

_embeddings = None

def get_retriever(collection_name="about_myself", k=2):
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )

    client = MongoClient(os.getenv("MONGO_ATLAS_LOCAL"))
    db = client["myself_db"]
    collection = db[collection_name]

    vectordb = MongoDBAtlasVectorSearch(
        embedding=_embeddings,
        collection=collection,
        index_name="vector_index",
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    return retriever