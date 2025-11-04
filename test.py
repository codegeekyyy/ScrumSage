import langchain
import langchain_community
import dotenv
import chromadb
import streamlit
import langchain_groq
from langchain_core.documents import Document 
print("all are done successfully")

from src.vector_store import create_vector_store

create_vector_store("data/updates.csv")
