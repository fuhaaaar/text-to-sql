from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_result(question, result):
    result_str = result.to_string(index=False)

    prompt = f"""A user asked this question about a business database:
"{question}"

The query returned this data:
{result_str}

In exactly one simple sentence, explain what this data means in plain English.
No technical terms, no mention of SQL or databases."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    from query_engine import ask

    question = "What are the top 5 most profitable products?"
    result, sql, error = ask(question)

    if error:
        print(f"Error: {error}")
    else:
        explanation = explain_result(question, result)
        print("Result:")
        print(result)
        print("\nExplanation:")
        print(explanation)
        