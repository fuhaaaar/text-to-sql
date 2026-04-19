import pandas as pd
import json
from datetime import datetime
from query_engine import ask
from explainer import explain_result

def run_evaluation():
    df = pd.read_csv("eval_questions.csv")
    
    results = []
    correct = 0
    failed = 0
    retried = 0
    total = len(df)

    print(f"Running evaluation on {total} questions...\n")

    for i, row in df.iterrows():
        question = row["question"]
        expected = str(row["expected_output_contains"]).lower()

        print(f"[{i+1}/{total}] {question}")

        result, sql, error = ask(question)

        if error:
            status = "FAILED"
            failed += 1
            print(f"  FAILED — {error}\n")
            results.append({
                "question": question,
                "expected": expected,
                "status": status,
                "sql": None,
                "error": error
            })
            continue

        result_str = result.to_string(index=False).lower()
        passed = expected in result_str

        if passed:
            status = "PASSED"
            correct += 1
            print(f"  PASSED\n")
        else:
            status = "FAILED"
            failed += 1
            print(f"  FAILED — expected '{expected}' not found in result\n")

        results.append({
            "question": question,
            "expected": expected,
            "status": status,
            "sql": sql,
            "error": None
        })

    accuracy = round((correct / total) * 100, 1)
    failure_rate = round((failed / total) * 100, 1)

    print("=" * 50)
    print(f"EVALUATION COMPLETE")
    print(f"Total questions : {total}")
    print(f"Passed          : {correct}")
    print(f"Failed          : {failed}")
    print(f"Accuracy        : {accuracy}%")
    print(f"Failure rate    : {failure_rate}%")
    print("=" * 50)

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total,
        "passed": correct,
        "failed": failed,
        "accuracy_percent": accuracy,
        "failure_rate_percent": failure_rate,
        "results": results
    }

    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nFull report saved to eval_report.json")
    return report

if __name__ == "__main__":
    run_evaluation()