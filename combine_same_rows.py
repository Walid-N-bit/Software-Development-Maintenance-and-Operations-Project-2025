import csv
import os


def annotate(annotated_file: str, file_to_annotate: str, annotated_dir: str):
    """
    Copies the annotations from the original file to a new one.
    Requires the new file to be smaller than the original, and the process with which
    the new file was produced HAS TO BE REDUCTIVE compared to the old one.
    Creates a directory named annotated if it doesn't exist, where the resulting csv file will be written.
    """
    annotated_csv = []
    new_csv = []

    with open(annotated_file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            annotated_csv.append(row)
    # First element is header, skip
    annotated_csv = annotated_csv[1:]

    with open(file_to_annotate, "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            new_csv.append(row)
    # First element is header, skip
    new_csv = new_csv[1:]

    # check if the new file is longer than the old one
    if len(new_csv) > len(annotated_csv):
        raise ValueError("New File is longer!")

    # Check if the old each of the lines in the new one
    check_new_csv = [line[1:] for line in new_csv]
    check_old_csv = [line[1:] for line in annotated_csv]

    print(check_new_csv)
    print(check_old_csv)

    for line in check_new_csv:
        print(line)
        if line not in check_old_csv:
            raise ValueError("New File contains unique data!")

    # If the row is otherwise the same except for true positive, use the same row from the already annotated file, and mark it true positive
    for row in annotated_csv:
        for i in range(len(new_csv)):
            if new_csv[i][1:] == row[1:]:
                new_csv[i] = row

    if not os.path.exists(annotated_dir):
        os.makedirs(annotated_dir)

    new_annotated_path = os.path.join(
        f"{annotated_dir}/{file_to_annotate.split('/')[1].split('.csv')[0]}_ANNOTATED.csv"
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


def main():
    # main annotated, the largest one
    annotated_file = "annotated/devs_similarity_no_c4c7_t=0.9_ANNOTATED.csv"
    # new, more strict, smaller one wihtout annotations
    file_to_annotate = "three.js-data/devs_similarity_no_c4c7__t=0.99.csv"
    # Directory to put annotated files in
    annotated_dir = "annotated"
    annotate(annotated_file, file_to_annotate, annotated_dir)


if __name__ == "__main__":
    main()
