from src.fetch_jira import fetch_jira_updates

# Replace "AI" with your actual Jira project key (you can find it in the Jira URL)
fetch_jira_updates(project_key="KAN", max_results=10)
