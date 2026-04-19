from sqlalchemy import create_engine, inspect

def get_schema():
    engine = create_engine("sqlite:///superstore.db")
    inspector = inspect(engine)
    
    schema = ""
    
    for table_name in inspector.get_table_names():
        schema += f"Table: {table_name}\n"
        schema += "Columns:\n"
        
        for column in inspector.get_columns(table_name):
            schema += f"  - {column['name']} ({column['type']})\n"
        
        schema += "\n"
    
    return schema

if __name__ == "__main__":
    print(get_schema())