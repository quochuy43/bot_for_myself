import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rag_for_me.retriever.hybrid_retriever import get_hybrid_retriever
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from rag_for_me.prompt import rag_prompt_template
from langchain_openai import ChatOpenAI

# IDF (inverse document frequency): độ hiếm của từ đó trên toàn bộ tập

load_dotenv()

prompt = ChatPromptTemplate.from_template(rag_prompt_template)

def format_docs(docs):
    formatted = "\n\n".join(f"[{doc.metadata['category']}]\n{doc.page_content}" for doc in docs)
    return formatted

def get_rag_chain():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
    )
    retriever = get_hybrid_retriever(alpha=0.5)
    return (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

if __name__ == "__main__":
    load_dotenv()

    rag_chain = get_rag_chain()

    print("🔍 RAG Chatbot is ready! Type your question (or 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            print("👋 Bye!")
            break

        try:
            answer = rag_chain.invoke(query)
            print(f"Bot: {answer}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")