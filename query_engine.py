from groq import Groq
from dotenv import load_dotenv
from schema_extractor import get_schema
from safety import is_safe, add_limit
from executor import run_query
from logger import log_query
import os

load_dotenv()
import streamlit as st

api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_sql(question, error=None):
    schema = get_schema()

    if error:
        prompt = f"""You are an expert SQL writer for SQLite databases.

Here is the database schema:
{schema}

Important rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Always use LIMIT 100 unless the user asks for more
- Column names have spaces so always wrap them in double quotes like "Order ID"
- Always include the actual numbers/values in the result, not just names
- For questions about highest/lowest/most/best, always include the metric you are sorting by

The previous query failed with this error:
{error}

Fix the query for this question:
{question}"""
    else:
        prompt = f"""You are an expert SQL writer for SQLite databases.

Here is the database schema:
{schema}

Important rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Always use LIMIT 100 unless the user asks for more
- Column names have spaces so always wrap them in double quotes like "Order ID"
- Always include the actual numbers/values in the result, not just names
- For questions about highest/lowest/most/best, always include the metric you are sorting by

Convert this question to SQL:
{question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    sql = response.choices[0].message.content.strip()
    return sql


def ask(question):
    max_retries = 2
    error = None
    retries = 0

    for attempt in range(max_retries + 1):
        sql = generate_sql(question, error=error)
        sql = add_limit(sql)

        safe, message = is_safe(sql)
        if not safe:
            log_query(question, sql, retries, message, False)
            return None, None, message

        try:
            result = run_query(sql)
            log_query(question, sql, retries, None, True)
            return result, sql, None

        except Exception as e:
            error = str(e)
            retries += 1
            if attempt == max_retries:
                log_query(question, sql, retries, error, False)
                return None, sql, f"Query failed after {max_retries} retries. Last error: {error}"

    return None, None, "Something went wrong."


if __name__ == "__main__":
    questions = [
        "Which city had the highest total sales?",
        "What are the top 5 most profitable products?",
        "DROP TABLE orders"
    ]

    for q in questions:
        print(f"\nQuestion: {q}")
        result, sql, error = ask(q)

        if error:
            print(f"Error: {error}")
        else:
            print(f"SQL: {sql}")
            print(result)