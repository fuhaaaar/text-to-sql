import json
import os
from datetime import datetime

LOG_FILE = "query_logs.json"

def log_query(question, sql, retries, error, success):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "generated_sql": sql,
        "retries": retries,
        "error": error,
        "success": success
    }

    logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)