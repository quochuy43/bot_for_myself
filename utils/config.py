import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

MODEL_NAME = "openai:gpt-4o-mini"
model=init_chat_model(MODEL_NAME, temperature=0.3)


# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# MODEL_NAME = "gemini-2.0-flash"
# model = ChatGoogleGenerativeAI(
#     model=MODEL_NAME,
#     temperature=0.2
# )