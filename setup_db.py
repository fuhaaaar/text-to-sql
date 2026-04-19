import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("Sample - Superstore.csv", encoding='windows-1252')

print("Columns in your dataset:")
print(df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))

engine = create_engine("sqlite:///superstore.db")

df.to_sql("orders", engine, if_exists="replace", index=False)

print("\nDatabase created successfully!")
print(f"Total rows loaded: {len(df)}")