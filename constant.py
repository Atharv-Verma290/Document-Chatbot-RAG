import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

PERSIST_DIR = "./chroma_db"

thread = {'configurable': {'thread_id': 'abc123'}}