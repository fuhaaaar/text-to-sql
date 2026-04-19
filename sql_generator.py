from groq import Groq
from dotenv import load_dotenv
from schema_extractor import get_schema
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question):
    schema = get_schema()
    
    prompt = f"""You are an expert SQL writer for SQLite databases.

Here is the database schema:
{schema}

Important rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Always use LIMIT 100 unless the user asks for more
- Column names have spaces so always wrap them in double quotes like "Order ID"

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


if __name__ == "__main__":
    question = "Which city had the highest total sales?"
    sql = generate_sql(question)
    print("Generated SQL:")
    print(sql)