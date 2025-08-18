import os
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = "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"

MODEL_NAME = "gpt-4o"
model = ChatOpenAI(model=MODEL_NAME)