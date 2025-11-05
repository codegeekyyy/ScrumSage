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
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ CSV not found at path: {csv_path}")

    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("❌ CSV is empty. Run fetch_jira_updates() first to populate data.")

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

    print(f"✅ Vector database created and saved in '{persist_directory}/'")
    return vector_db


def get_relevant_updates(query, persist_directory="chroma_db", k=5, method="mmr"):
    """
    Retrieve semantically relevant updates using advanced retrieval strategies:
    - 'mmr'  → Max Marginal Relevance (balanced diversity + relevance)
    - 'similarity' → Classic cosine similarity search
    - 'hybrid' → Combines both approaches
    """
    load_dotenv()

    # Load embeddings and vector database
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    print(f"🔍 Using retrieval method: {method.upper()} (k={k})")

    # --- Retrieval Strategies ---
    if method == "mmr":
        # Max Marginal Relevance - balances diversity and relevance
        res = vector_db.max_marginal_relevance_search(query, k=k, fetch_k=10)

    elif method == "hybrid":
        # Combine both similarity and MMR for richer context
        sim_res = vector_db.similarity_search(query, k=k)
        mmr_res = vector_db.max_marginal_relevance_search(query, k=k, fetch_k=10)

        # Merge while avoiding duplicates
        seen = set()
        res = []
        for r in sim_res + mmr_res:
            key = r.page_content
            if key not in seen:
                seen.add(key)
                res.append(r)
        res = res[:k]

    else:
        # Default similarity search
        res = vector_db.similarity_search(query, k=k)

    if not res:
        print("⚠️ No relevant updates found for your query. Try increasing 'k' or using 'hybrid' method.")

    return res
