from src.vector_store import get_relevant_updates
from datetime import date
import pandas as pd
import os


def run_ai_pipeline(query=None):
    """
    Main AI pipeline:
    1. Try retrieving relevant updates from vector DB.
    2. If empty or failed, fall back to CSV.
    3. Send all updates to summarizer.
    4. Return final AI-generated stand-up report.
    """
    if query is None:
        today = date.today().strftime("%Y-%m-%d")
        query = f"Summarize all Jira updates for {today}, including Done, In Progress, and To Do tasks"

    print(f"🔍 Retrieving data for query: {query}\n")

    try:
        res = get_relevant_updates(query)
    except Exception as e:
        print(f"⚠️ Vector retrieval failed: {e}")
        res = []

    # ✅ If vector search failed or returned nothing, use CSV fallback
    if not res:
        print("⚠️ No vector results found. Using fallback: data/updates.csv\n")
        if os.path.exists("data/updates.csv"):
            df = pd.read_csv("data/updates.csv")
            text = "\n".join([f"{r['name']}: {r['update']}" for _, r in df.iterrows()])
        else:
            print("❌ No CSV found either. Please run fetch_jira.py first.")
            return
    else:
        text = "\n".join([f"{doc.metadata['name']}: {doc.page_content}" for doc in res])

    print("🧠 Generating AI Stand-Up Summary...\n")
    print("📝 DEBUG: Text sent to model:\n", text)
    report = generate_standup_report_from_text(text)
    return report


def generate_standup_report_from_text(text):
    """
    Wrapper to use LangChain + Groq LLM for structured summarization.
    """
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq
    from dotenv import load_dotenv

    load_dotenv()
    import os
    groq_api_key = os.getenv("GROQ_API_KEY")

    prompt = PromptTemplate(
        template=(
            "You are an AI Scrum Master. You will receive developer updates extracted from Jira "
            "in the form '<name>: <issue_key>: <summary> (Status: <status>)'.\n\n"
            "Use ONLY the provided updates. Do not invent new names or tasks.\n\n"
            "Generate a Markdown-formatted report with the following sections:\n\n"
            "### ✅ Tasks Completed (Done)\n"
            "- List all updates where Status = 'Done'\n\n"
            "### ⚙️ Tasks In Progress\n"
            "- List all updates where Status = 'In Progress'\n\n"
            "### 🗓️ Tasks Planned (To Do)\n"
            "- List all updates where Status = 'To Do'\n\n"
            "### 🧱 Blockers\n"
            "- If any update mentions blockers, show them; otherwise, write 'None'.\n\n"
            "### 📊 Overall Summary\n"
            "- Summarize overall progress, achievements, and next focus.\n\n"
            "Developer Updates:\n{developer_updates}\n\n"
            "Now write the full stand-up report using only this data."
        ),
        input_variables=["developer_updates"],
    )

    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, groq_api_key=groq_api_key)
    chain = prompt | model
    result = chain.invoke({"developer_updates": text})
    return result.content
