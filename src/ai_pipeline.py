from src.vector_store import get_relevant_updates
from datetime import date

def run_ai_pipeline(query=None):
    """
    Main AI pipeline:
    1. Retrieve relevant updates from vector DB.
    2. Send them to the summarizer.
    3. Return final AI-generated stand-up report.
    """
    if query is None:
        today = date.today().strftime("%Y-%m-%d")
        query = f"summarize updates from {today}"

    print(f"🔍 Retrieving data for query: {query}\n")
    res = get_relevant_updates(query)

    if not res:
        print("⚠️ No relevant updates found for your query.")
        return

    # Combine retrieved text for summarization
    retrieved_text = "\n".join(
        [f"{doc.metadata['name']}: {doc.page_content}" for doc in res]
    )

    print("🧠 Generating AI Stand-Up Summary...\n")
    report = generate_standup_report_from_text(retrieved_text)
    return report


def generate_standup_report_from_text(text):
    """
    Wrapper function to use the same LangChain summarization logic,
    but directly from text instead of CSV file.
    """
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq  
    from dotenv import load_dotenv
    import os

    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    prompt = PromptTemplate(
    template=(
        "You are an AI Scrum Master. You will receive developer updates extracted directly from Jira "
        "in the form: '<name>: <issue_key>: <summary> (Status: <status>)'.\n\n"
        "Use only the provided updates. Do not invent new names, tasks, or data.\n\n"
        "Your job is to generate a structured Markdown report with these sections:\n\n"
        "### ✅ Tasks Completed (Done)\n"
        "- List all tasks whose status = 'Done'.\n\n"
        "### ⚙️ Tasks In Progress\n"
        "- List all tasks whose status = 'In Progress'.\n\n"
        "### 🗓️ Tasks Planned (To Do)\n"
        "- List all tasks whose status = 'To Do'.\n\n"
        "### 🧱 Blockers\n"
        "- If any update mentions blockers, report them. Otherwise, say 'None'.\n\n"
        "### 📊 Overall Summary\n"
        "- Provide a concise summary of overall project progress, recent accomplishments, "
        "and focus areas for the upcoming days based on the data provided.\n\n"
        "Developer Updates:\n{developer_updates}\n\n"
        "Now write the full stand-up report using only this data."
    ),
    input_variables=["developer_updates"],
)

    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, groq_api_key=groq_api_key)
    # runnable
    chain=prompt|model

    result = chain.invoke({"developer_updates":text})
    return result.content
