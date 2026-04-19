DANGEROUS_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE", "CREATE"]

def is_safe(sql):
    sql_upper = sql.upper()
    
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in sql_upper:
            return False, f"Blocked: query contains '{keyword}' which is not allowed."
    
    return True, "OK"

def add_limit(sql):
    if "LIMIT" not in sql.upper():
        sql = sql.rstrip(";")
        sql = sql + " LIMIT 100"
    return sql


if __name__ == "__main__":
    good_query = 'SELECT "City", SUM("Sales") FROM orders GROUP BY "City"'
    bad_query = 'DROP TABLE orders'
    
    print(is_safe(good_query))
    print(is_safe(bad_query))
    print(add_limit(good_query))