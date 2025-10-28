import csv
import os

# Moves the annotations to the new file
# Requires the new file to be smaller and whatever has been done to it has to be purely reductive
# e.g. the same row has to exist in both, then it is annotated the same as the old one.

# main annotated, the largest one
annotated_path = ""
# new, more strict, smaller one wihtout annotations
new_path = ""

annotated_csv = []
new_csv = []

with open(annotated_path, "r", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        annotated_csv.append(row)
# First element is header, skip
annotated_csv = annotated_csv[1:]

with open(new_path, "r", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        new_csv.append(row)
# First element is header, skip
new_csv = new_csv[1:]

# If the row is otherwise the same except for true positive, use the same row from the already annotated file, and mark it true positive
# The "old" annotated csv has to be longer, and it most likely is.
for row in annotated_csv:
    for i in range(len(new_csv)):
        if new_csv[i][1:] == row[1:]:
            new_csv[i] = row

# need to have folder named annotated or change to whatever
new_annotated_path = os.path.join(
    f"annotated/{new_path.split("/")[1].split(".")[0]}_ANNOTATED.csv"
)

# Expects no c4 -c7
with open(new_annotated_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",", quotechar='"')
    writer.writerow(
        [
            "true_pos",
            "name_1",
            "email_1",
            "name_2",
            "email_2",
            "c1",
            "c2",
            "c3.1",
            "c3.2",
        ]
    )
    writer.writerows(new_csv)
