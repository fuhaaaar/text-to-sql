from sqlalchemy import create_engine, text
import pandas as pd

def run_query(sql):
    engine = create_engine("sqlite:///superstore.db")
    
    with engine.connect() as connection:
        result = pd.read_sql_query(text(sql), connection)
    
    return result


if __name__ == "__main__":
    sql = 'SELECT "City", SUM("Sales") as Total_Sales FROM orders GROUP BY "City" ORDER BY Total_Sales DESC LIMIT 10'
    
    result = run_query(sql)
    print(result)