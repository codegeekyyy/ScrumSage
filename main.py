import os
from datetime import datetime
from src.fetch_jira import fetch_jira_updates
from src.vector_store import create_vector_store
from src.ai_pipeline import run_ai_pipeline

def main():
    print("🧠 AI Stand-Up Report Generator\n")

    # 1️⃣ Fetch latest Jira issues
    print("📡 Fetching latest Jira updates...")
    df = fetch_jira_updates(project_key="KAN", max_results=20)

    if df.empty:
        print("⚠️ No Jira updates found. Please check your Jira project or API credentials.")
        return

    print(f"✅ Retrieved {len(df)} issues from Jira.")

    # 2️⃣ Create or update the vector store
    print("🧩 Building vector database...")
    create_vector_store("data/updates.csv")

    # 3️⃣ Run AI summarization pipeline
    print("🧠 Generating AI Stand-Up Report...\n")
    report = run_ai_pipeline()

    # 4️⃣ Save the report with timestamp
    if report:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = f"reports/standup_report_{timestamp}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved as: {report_path}\n")

        print("📋 AI-Generated Stand-Up Report:\n")
        print(report)
    else:
        print("⚠️ No report generated.")

if __name__ == "__main__":
    main()
