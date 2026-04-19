import streamlit as st
from query_engine import ask
from explainer import explain_result
import os
from sqlalchemy import create_engine
import pandas as pd

if not os.path.exists("superstore.db"):
    df = pd.read_csv("Sample - Superstore.csv", encoding='windows-1252')
    engine = create_engine("sqlite:///superstore.db")
    df.to_sql("orders", engine, if_exists="replace", index=False)

st.set_page_config(page_title="Superstore Data Assistant", page_icon="🛒")

st.title("Superstore Data Assistant")
st.write("Ask any question about the Superstore sales data in plain English.")

st.markdown("**Example questions you can ask:**")
st.markdown("- Which city had the highest total sales?")
st.markdown("- What are the top 5 most profitable products?")
st.markdown("- How many orders were placed in each region?")
st.markdown("- Which product category has the highest discount on average?")

st.divider()

question = st.text_input("Type your question here:", placeholder="e.g. Which state had the lowest profit?")

show_sql = st.toggle("Show generated SQL")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        with st.spinner("Thinking..."):
            result, sql, error = ask(question)

        if error:
            st.error(f"{error}")
        else:
            if show_sql:
                st.subheader("Generated SQL")
                st.code(sql, language="sql")

            st.subheader("Result")
            st.dataframe(result)

            st.subheader("Summary")
            with st.spinner("Summarizing..."):
                explanation = explain_result(question, result)
            st.success(explanation)