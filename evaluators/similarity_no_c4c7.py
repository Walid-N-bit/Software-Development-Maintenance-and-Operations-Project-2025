import os
import pandas as pd
from itertools import combinations
from .similarity_default import bird_c1_c3
from tools.helpers import most_common_prefixes


def similarity_no_c4c7(
    devs: list[list[str]],
    data_folder: str,
    email_check: bool,
    generic_prefixes: set[str],
    thresholds: list[float],
):
    """
    Calculates similarity between developer name pairs using the Bird heuristic.

    This function compares all possible pairs of developers and evaluates three conditions
    from the Bird heuristic (c1-c3) to identify potential duplicate identities. Results
    are filtered by similarity thresholds and saved to CSV files for manual review.

    Args
    ------
        devs : list[list[str]]
            List of developer lists containing ["name", "email"].
        data_folder : str
            Base folder path where output CSV files will be saved (as "{folder}-data").
        email_check : bool
            If True, email prefixes matching generic domains are excluded from similarity checks.
        threshholds : list[float]
            List of similarity threshold values (0.0-1.0) to generate separate filtered outputs.

    Outputs
    -------
        devs_similarity.csv
            All developer pairs with their similarity scores
        devs_similarity_no_c4c7_t={threshold}.csv
            Filtered pairs meeting threshold criteria (one per threshold)
    """
    SIMILARITY = []

    for dev_a, dev_b in combinations(devs, 2):
        c1, c2, c31, c32, email_a, email_b = bird_c1_c3(
            dev_a, dev_b, generic_prefixes, email_check
        )

        # Similarity without c4 - c7
        SIMILARITY.append([dev_a[0], email_a, dev_b[0], email_b, c1, c2, c31, c32])

    print(f"\nnoc4c7 Bird, email check = {str(email_check)}")
    print(f"Pairs: {len(SIMILARITY)}")
    print("____________")

    # Save data on all pairs (might be too big -> comment out to avoid)
    cols = [
        "name_1",
        "email_1",
        "name_2",
        "email_2",
        "c1",
        "c2",
        "c3.1",
        "c3.2",
    ]
    df = pd.DataFrame(SIMILARITY, columns=cols)

    df.to_csv(
        os.path.join(f"{data_folder}", "devs_similarity.csv"),
        index=False,
        header=True,
    )

    # Set similarity threshold, check c1-c3 against the threshold
    # a csv file will be created for every threshold value, you may add or edit to the list
    for t in thresholds:
        print("Threshold:", t)
        df["c1_check"] = df["c1"] >= t
        df["c2_check"] = df["c2"] >= t
        df["c3_check"] = (df["c3.1"] >= t) & (df["c3.2"] >= t)
        # Keep only rows where at least one condition is True

        df = df[df[["c1_check", "c2_check", "c3_check"]].any(axis=1)]

        print(f"Limited Pairs: {len(df)}")
        print("__________________________")

        # Omit "check" columns, save to csv
        df = df[
            [
                "name_1",
                "email_1",
                "name_2",
                "email_2",
                "c1",
                "c2",
                "c3.1",
                "c3.2",
            ]
        ]

        # Add empty column for manual annotation
        df.insert(0, "true_pos", 0)

        df.to_csv(
            os.path.join(
                f"{data_folder}",
                f"devs_similarity_no_c4c7{"_email_check=" if email_check else ""}{len(generic_prefixes) if email_check else ""}_t={t}.csv",
            ),
            index=False,
            header=True,
        )
