from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from rag_for_me.build_vector.loader.document_loader import split_markdown_by_heading
from pymongo import MongoClient

import os
from dotenv import load_dotenv
load_dotenv()
 
def create_vector_store(docs, collection_name="about_myself"):
    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model="models/embedding-001", 
    #     google_api_key=os.getenv("GOOGLE_API_KEY")
    # )
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY") 
    )
 
    client = MongoClient(os.getenv("MONGO_ATLAS"))
    db = client["vector_store"]
    collection = db[collection_name]
 
    vectordb = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index"
    )
    return vectordb


def get_embeddings():
    # return GoogleGenerativeAIEmbeddings(
    #     model="models/embedding-001",
    #     google_api_key=os.getenv("GOOGLE_API_KEY")
    # )
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )

def load_vector_store(collection_name="about_myself"):
    client = MongoClient(os.getenv("MONGO_ATLAS"))
    db = client["vector_store"]
    collection = db[collection_name]

    vectordb = MongoDBAtlasVectorSearch(
        embedding=get_embeddings(),
        collection=collection,
        index_name="vector_index"
    )
    return vectordb
 
if __name__ == "__main__":

    # Create DB
    docs = split_markdown_by_heading()
    vectorstore = create_vector_store(docs, collection_name="about_myself")

    # Test
    # vectorstore = load_vector_store(collection_name="about_myself")
    # query = "What is Huy's birthday?"
    # results = vectorstore.similarity_search(query, k=2)
    # print("\n🔎 Query:", query)
    # for r in results:
    #     print("->", r.page_content, "| category:", r.metadata["category"])