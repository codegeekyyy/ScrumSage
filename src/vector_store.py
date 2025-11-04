import os
import pandas as pd
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv


def create_vector_store(csv_path="data/updates.csv", persist_directory="chroma_db"):
    """
    Create a Chroma vector database from developer updates.
    Each row in the CSV becomes a document with text embeddings.
    """
    load_dotenv()

    # Load CSV file
    df = pd.read_csv(csv_path)

    # Convert each update into a LangChain Document with metadata
    documents = [
        Document(
            page_content=row["update"],
            metadata={"name": row["name"], "date": row["date"]}
        )
        for _, row in df.iterrows()
    ]

    # Create embeddings and store them in Chroma
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    # vector_db.persist()
    print(f"✅ Vector database created and saved in '{persist_directory}/'")
    return vector_db


def get_relevant_updates(query, persist_directory="chroma_db", k=5):
    """
    Retrieve the most semantically relevant updates from Chroma for a given query.
    Example query: 'Summarize today's updates' or 'What did Alice do this week?'
    """
    load_dotenv()

    # Load embeddings and vector database
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    # Perform semantic search
    res = vector_db.similarity_search(query, k=k)
    return res
