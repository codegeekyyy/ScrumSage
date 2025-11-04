# 🧠 AI Stand-Up Report Generator

### An AI-powered daily report generator that summarizes developer progress from Jira tasks using LLMs

---

## 🚀 Overview

The **AI Stand-Up Report Generator** automatically fetches tasks from your **Jira board** (using the Jira REST API), processes them using a **vector database**, and then uses an **LLM (Groq + LangChain)** to generate a structured **daily stand-up report** — including sections like:

- ✅ **Tasks Completed (Done)**
- ⚙️ **Tasks In Progress**
- 🗓️ **Tasks Planned (To Do)**
- 🧱 **Blockers**
- 🧾 **Overall Summary**

This tool helps teams **automate their daily reports**, **save time**, and **keep project tracking transparent**.

---

## 🏗️ Project Structure

AI_report_generator/
│
├── data/
│ └── updates.csv ← Stores task data fetched from Jira
│
├── src/
│ ├── ai_pipeline.py ← Main AI logic: summarize + generate reports
│ ├── vector_store.py ← Handles vector embeddings and document search
│ ├── summarize.py ← Summarization helper (standalone CSV-based)
│ ├── fetch_jira.py ← Fetches Jira issues dynamically
│ ├── init.py
│
├── .env ← Stores Jira + Groq API keys (ignored by Git)
├── requirements.txt ← Python dependencies
├── main.py ← Entry point to generate daily report
├── test.py ← Optional: build vector store manually
└── README.md ← Documentation (you’re reading it!)




---

## ⚙️ Features

✅ Fetches latest **Jira issues** (To Do, In Progress, Done)  
✅ Converts Jira task updates into structured data  
✅ Uses **LangChain + Groq LLM** to generate natural-language summaries  
✅ Embeds and retrieves data using **HuggingFace + Chroma vector store**  
✅ Supports **dynamic Jira project selection**  
✅ Produces detailed stand-up reports with an **AI-written summary**

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following:

```bash
# Jira configuration
JIRA_DOMAIN=https://your-domain.atlassian.net
JIRA_EMAIL=youremail@example.com
JIRA_API_TOKEN=your_api_token_here

# Groq API key (for LLM)
GROQ_API_KEY=your_groq_api_key_here

📝 To get Jira credentials:
Go to Atlassian API Tokens
Click Create API Token and copy it.
Use your Atlassian email as JIRA_EMAIL.
Find your Jira domain like https://yourname.atlassian.net.


🧩 Step-by-Step Workflow
Step 1 — Fetch Jira Data
Fetch the latest issues from your Jira project and save them into data/updates.csv.
python -c "from src.fetch_jira import fetch_jira_updates; fetch_jira_updates()"
✔ Automatically detects your Jira project
✔ Saves issues (with names, summaries, statuses, and dates)

Step 2 — Build Vector Store
Once updates.csv is ready, build a Chroma vector database:
python test.py


Step 3 — Generate the AI Stand-Up Report
Now generate the full AI-powered summary:
python main.py


Example Output-
🧠 Generating AI Stand-Up Report...

🔍 Retrieving data for query: summarize updates from 2025-11-04

🧠 Generating AI Stand-Up Summary...

📋 AI-Generated Stand-Up Report:

✅ Tasks Completed (Done)
- Alice: Fixed login issue (KAN-3)
- Bob: Deployed build to staging

⚙️ Tasks In Progress
- Charlie: Working on database schema

🗓️ Tasks Planned (To Do)
- Diana: Begin frontend refactoring

🧱 Blockers
- None



🧭 Dynamic Project Selection

If you have multiple Jira projects, the system automatically:

Detects available projects using /rest/api/3/project/search

Lets you choose which project to summarize

Or auto-selects the first one if you prefer hands-off mode

🧰 Tech Stack

Python 3.10+

LangChain + Groq LLM

HuggingFace Embeddings

Chroma Vector Store

Pandas

Jira REST API (v3)

Dotenv for secure environment handling

👨‍💻 Author

Harshdeep Singh
AI/ML Developer • B.Tech CSE @ Pranveer Singh Institute of Technology
📧 harshdeep.s5423@gmail.com

📜 License

This project is licensed under the MIT License — feel free to use, modify, and share.
