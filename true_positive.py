import csv
import os

# Calculates the true positive rate for all csv files in a folder

annotated_path = "annotated"

files = os.listdir(annotated_path)

for file in files:
    rows = []
    with open(os.path.join(annotated_path, file), "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            rows.append(row)
    # First element is header, skip
    rows = rows[1:]
    pos = len(rows)
    tp = len([row for row in rows if int(row[0]) == 1])
    print(f"P: {pos}, TP: {tp}, FP: {pos - tp}, Ratio: {tp/pos:.2f}, File: {file}")
