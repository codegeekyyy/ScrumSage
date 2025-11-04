# import os
# import pandas as pd
# from langchain import PromptTemplate, LLMChain
# from dotenv import load_dotenv, find_dotenv
# from langchain_groq import ChatGroq


# def generate_standup_report(csv_path="data/updates.csv"):
#     """
#     Generates an AI-powered daily stand-up report from developer updates.
#     """
#     load_dotenv(find_dotenv())

#     groq_api_key = os.getenv("GROQ_API_KEY")
#     if not groq_api_key:
#         raise ValueError("GROQ_API_KEY not found in .env file")

#     if not os.path.exists(csv_path):
#         raise FileNotFoundError(f"CSV file not found: {csv_path}")

#     df = pd.read_csv(csv_path)

#     developer_updates = "\n".join(
#         [f"{row['name']}: {row['update']}" for _, row in df.iterrows()]
#     )

#     prompt = PromptTemplate(
#         template=(
#             "You are an AI Scrum Master. Summarize the following developer updates "
#             "into a daily stand-up report with sections: Yesterday, Today, and Blockers.\n\n"
#             "Developer Updates:\n{developer_updates}\n\n"
#             "Now write the report:"
#         ),
#         input_variables=["developer_updates"],
#     )

#     model = ChatGroq(
#         model="llama-3.1-8b-instant",
#         temperature=0.3,
#         groq_api_key=groq_api_key
#     )
#     chain = LLMChain(prompt=prompt, llm=model)

#     res = chain.run(developer_updates=developer_updates)
#     return res.strip()
