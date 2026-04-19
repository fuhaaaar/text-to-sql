# Natural Language Data Assistant (Text-to-SQL)

A web app that lets users query a business database in plain English — no SQL knowledge needed.

## What it does
- User types a question like "which city had the highest sales?"
- App converts it to SQL automatically using an LLM
- Runs the query on a real Superstore sales database
- Returns the result as a table with a plain English summary

## Edge cases handled
- **Hallucinated columns** — if the LLM generates invalid SQL, a self-healing retry loop sends the error back to the LLM to fix it automatically
- **Destructive queries** — DROP, DELETE, UPDATE, INSERT are blocked before reaching the database
- **Read-only database** — database connection is restricted to SELECT only
- **Large result sets** — LIMIT is automatically added to every query

## Tech stack
- Python
- Streamlit (UI)
- Groq API with Llama 3.3 70B (LLM)
- SQLite + SQLAlchemy (database)
- Pandas (data handling)

## How to run locally

1. Clone the repo
2. Install dependencies
   pip install streamlit groq pandas sqlalchemy python-dotenv openpyxl
3. Create a .env file and add your Groq API key
   GROQ_API_KEY=your_key_here
4. Run the app
   streamlit run app.py

## Dataset
Superstore Sales dataset — 9,994 rows of real business sales data including orders, products, customers and regions.

## Sample questions to try
- Which region had the highest total profit?
- What are the top 5 most profitable products?
- Which sub-category had the highest average discount?
- How many orders were placed in each state?