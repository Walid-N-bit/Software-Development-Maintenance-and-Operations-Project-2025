import csv
import os


def calc_tp(annotated_path: str) -> list[str | None]:
    """
    Calculates the true positive rate for all eligible .csv files in a folder.
    """
    files = os.listdir(annotated_path)
    results = []
    for file in files:
        if file.endswith(".csv"):
            rows = []
            with open(os.path.join(annotated_path, file), "r", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for row in reader:
                    rows.append(row)
            headers = rows[0]
            # Filter out non-annotated
            if headers[0] != "true_pos":
                results.append(None)
                continue
            # First element is header, skip
            rows = rows[1:]
            pos = len(rows)
            tp = len([row for row in rows if int(row[0]) == 1])
            results.append(
                f"P: {pos}, TP: {tp}, FP: {pos - tp}, Ratio: {tp/pos:.2f}, File: {file}"
            )
    return results


def main():
    annotated_path = "annotated"
    for result in calc_tp(annotated_path):
        if result:
            print(result)


if __name__ == "__main__":
    main()
