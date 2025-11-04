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



