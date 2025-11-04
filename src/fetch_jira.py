import os
import requests
import pandas as pd
from dotenv import load_dotenv

def fetch_jira_updates(project_key="KAN", max_results=10, jql_override=None):
    """
    Fetch recent issues from a Jira Cloud project using JQL.
    Includes proper status handling for To Do, In Progress, and Done.
    """
    load_dotenv()
    jira_domain = os.getenv("JIRA_DOMAIN")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")

    if not all([jira_domain, jira_email, jira_token]):
        raise ValueError("❌ Missing one or more Jira credentials in .env")

    url = f"{jira_domain}/rest/api/3/search/jql"
    jql_query = jql_override or f'project = "{project_key}" ORDER BY updated DESC'

    body = {
        "jql": jql_query,
        "maxResults": min(100, max_results),
        "fields": ["summary", "assignee", "updated", "status"]
    }

    auth = (jira_email, jira_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print(f"🔎 Jira search endpoint: {url}")
    print(f"🧩 JQL: {jql_query}")

    resp = requests.post(url, headers=headers, json=body, auth=auth, timeout=30)
    if resp.status_code != 200:
        print("⚠️ Jira API error:", resp.status_code)
        print("Response:", resp.text)
        resp.raise_for_status()

    issues = resp.json().get("issues", [])
    data = []

    for issue in issues:
        fields = issue.get("fields", {})
        assignee = (fields.get("assignee") or {}).get("displayName", "Unassigned")
        summary = fields.get("summary", "")
        updated = fields.get("updated", "")[:10]

        # ✅ Extract both status name and category
        status_field = fields.get("status") or {}
        status_name = status_field.get("name", "Unknown")
        status_category = status_field.get("statusCategory", {}).get("name", "").lower()

        # Normalize to 3 simple categories
        if "progress" in status_category:
            status_final = "In Progress"
        elif "done" in status_category or "complete" in status_category:
            status_final = "Done"
        elif "to do" in status_category or "new" in status_category:
            status_final = "To Do"
        else:
            status_final = status_name  # fallback to original Jira label

        update_text = f"{issue.get('key','')}: {summary} (Status: {status_final})"

        data.append({
            "name": assignee,
            "update": update_text,
            "date": updated
        })

    # Save to CSV
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/updates.csv", index=False)

    print(f"✅ Saved {len(df)} Jira issues to data/updates.csv")
    return df
