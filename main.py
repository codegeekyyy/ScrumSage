from src.ai_pipeline import run_ai_pipeline

if __name__== "__main__":
    print("🧠 Generating AI Stand-Up Report...\n")
    report = run_ai_pipeline()
    print("📋 AI-Generated Stand-Up Report:\n")
    print(report)