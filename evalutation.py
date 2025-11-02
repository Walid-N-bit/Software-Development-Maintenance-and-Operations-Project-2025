import os
import pandas as pd
from itertools import combinations
from Levenshtein import ratio as sim
from tools import process, most_common_prefixes


def bird_c1_c3(
    dev_a: list[str],
    dev_b: list[str],
    generic_prefixes: set[str],
    email_check: bool,
):
    """
    Calculates the first three conditions of the Bird heuristic.
    """
    name_a, first_a, last_a, _, _, email_a, prefix_a = process(dev_a)
    name_b, first_b, last_b, _, _, email_b, prefix_b = process(dev_b)
    # Conditions of Bird heuristic
    c1 = sim(name_a, name_b)
    # CHECK FOR A SAME EMAIL-PREFIX
    if (prefix_a in generic_prefixes or prefix_b in generic_prefixes) and email_check:
        c2 = 0
    else:
        c2 = sim(prefix_a, prefix_b)
    c31 = sim(first_a, first_b)
    c32 = sim(last_a, last_b)

    return c1, c2, c31, c32, email_a, email_b


def bird_c4_c7(dev_a: list[str], dev_b: list[str]):
    """
    Calculates conditions c4 to c7 of the Bird heuristic.
    """
    _, first_a, last_a, i_first_a, i_last_a, _, prefix_a = process(dev_a)
    _, first_b, last_b, i_first_b, i_last_b, _, prefix_b = process(dev_b)
    c4 = c5 = c6 = c7 = False
    # Since lastname and initials can be empty, perform appropriate checks
    if i_first_a != "" and last_a != "":
        c4 = i_first_a in prefix_b and last_a in prefix_b

    if i_last_a != "":
        c5 = i_last_a in prefix_b and first_a in prefix_b

    if i_first_b != "" and last_b != "":
        c6 = i_first_b in prefix_a and last_b in prefix_a

    if i_last_b != "":
        c7 = i_last_b in prefix_a and first_b in prefix_a

    return c4, c5, c6, c7


def similarity_default(
    devs: list[list[str]],
    data_folder: str,
    email_check: bool,
    generic_prefixes: set[str],
    thresholds: list[float],
):
    """
    Calculates similarity between developer name pairs using the Bird heuristic.

    This function compares all possible pairs of developers and evaluates seven conditions
    from the Bird heuristic (c1-c7) to identify potential duplicate identities. Results
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
    ------
        devs_similarity.csv
            All developer pairs with their similarity scores
        devs_similarity_t={threshold}.csv
            Filtered pairs meeting threshold criteria (one per threshold)
    """
    SIMILARITY = []

    for dev_a, dev_b in combinations(devs, 2):
        # Pre-process both developers
        c1, c2, c31, c32, email_a, email_b = bird_c1_c3(
            dev_a, dev_b, generic_prefixes, email_check
        )

        c4, c5, c6, c7 = bird_c4_c7(dev_a, dev_b)

        # Save similarity data for each conditions. Original names are saved
        SIMILARITY.append(
            [dev_a[0], email_a, dev_b[0], email_b, c1, c2, c31, c32, c4, c5, c6, c7]
        )
    print(f"\nDefault bird, email check = {str(email_check)}")
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
        "c4",
        "c5",
        "c6",
        "c7",
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

        df = df[
            df[
                [
                    "c1_check",
                    "c2_check",
                    "c3_check",
                    "c4",
                    "c5",
                    "c6",
                    "c7",
                ]
            ].any(axis=1)
        ]

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
                "c4",
                "c5",
                "c6",
                "c7",
            ]
        ]

        # Add empty column for manual annotation
        df.insert(0, "true_pos", 0)

        df.to_csv(
            os.path.join(
                f"{data_folder}",
                f"devs_similarity{"_email_check=" if email_check else ""}{len(generic_prefixes) if email_check else ""}_t={t}.csv",
            ),
            index=False,
            header=True,
        )


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


from pyjarowinkler.distance import get_jaro_winkler_similarity as jaro_win_sim


def jaro_c1_c4(
    dev_a: list[str], dev_b: list[str], generic_prefixes: set[str], email_check: bool
):
    # Pre-process both developers
    name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = process(dev_a)
    name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = process(dev_b)

    # Conditions
    c1 = jaro_win_sim(name_a, name_b, ignore_case=True)
    if (prefix_a in generic_prefixes or prefix_b in generic_prefixes) and email_check:
        c2 = 0
    else:
        c2 = jaro_win_sim(prefix_a, prefix_b, ignore_case=True)

    c3 = 0
    c4 = 0
    if i_first_a != "" and last_a != "" and i_first_b != "" and last_b != "":
        c3 = jaro_win_sim(
            "".join((i_first_a, last_a)),
            "".join((i_first_b, last_b)),
            ignore_case=True,
        )
    if i_last_a != "" and first_a != "" and i_last_b != "" and first_b != "":
        c4 = jaro_win_sim(
            "".join((i_last_a, first_a)),
            "".join((i_last_b, first_b)),
            ignore_case=True,
        )
    return c1, c2, c3, c4, email_a, email_b


def similarity_jw_bird(
    devs: list[list[str]],
    data_folder: str,
    email_check: bool,
    generic_prefixes: set[str],
    thresholds: list[float],
):
    """
    Calculates similarity between developer name pairs using a modified Bird heuristic.
    Jaro-Winkler Distance is used to measure similarity between strings.

    The function compares all possible pairs of developers and evaluates the following conditions:
    c1: sim(name1, name2) >= t
    c2: sim(prefix1, prefix2) >= t
    c3: sim(i_first_name1+last_name1, i_first_name2+last_name2) >= t
    c4: sim(i_last_name1+first_name1, i_last_name2+first_name2) >= t

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
    ------
        devs_similarity.csv
            All developer pairs with their similarity scores
        devs_similarity_t={threshold}.csv
            Filtered pairs meeting threshold criteria (one per threshold)
    """
    SIMILARITY = []

    for dev_a, dev_b in combinations(devs, 2):
        c1, c2, c3, c4, email_a, email_b = jaro_c1_c4(
            dev_a, dev_b, generic_prefixes, email_check
        )
        # Save similarity data for each conditions. Original names are saved
        SIMILARITY.append([dev_a[0], email_a, dev_b[0], email_b, c1, c2, c3, c4])

    print(f"\nJaro-winkler bird, email check = {str(email_check)}")
    print(f"Pairs: {len(SIMILARITY)}")
    print("____________")

    # Save data on all pairs
    cols = [
        "name_1",
        "email_1",
        "name_2",
        "email_2",
        "c1",
        "c2",
        "c3",
        "c4",
    ]
    df = pd.DataFrame(SIMILARITY, columns=cols)

    df.to_csv(
        os.path.join(f"{data_folder}", "devs_jw_similarity.csv"),
        index=False,
        header=True,
    )
    # Set similarity threshold, check c1-c4 against the threshold
    # a csv file will be created for every threshold value, you may add or edit to the list
    for t in thresholds:
        print("Threshold:", t)
        df["c1_check"] = df["c1"] >= t
        df["c2_check"] = df["c2"] >= t
        df["c3_check"] = df["c3"] >= t
        df["c4_check"] = df["c4"] >= t

        # Keep only rows where at least one condition is True

        df = df[
            df[
                [
                    "c1_check",
                    "c2_check",
                    "c3_check",
                    "c4_check",
                ]
            ].any(axis=1)
        ]

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
                "c3",
                "c4",
            ]
        ]

        # Add empty column for manual annotation
        df.insert(0, "true_pos", 0)

        df.to_csv(
            os.path.join(
                f"{data_folder}",
                f"devs_jw_similarity{"_email_check=" if email_check else ""}{len(generic_prefixes) if email_check else ""}_t={t}.csv",
            ),
            index=False,
            header=True,
        )


def similarity_no_c4c7_email_improved(
    devs: list[list[str]],
    data_folder: str,
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
        name_a, first_a, last_a, _, _, email_a, prefix_a = process(dev_a)
        name_b, first_b, last_b, _, _, email_b, prefix_b = process(dev_b)
        # Conditions of Bird heuristic
        c1 = sim(name_a, name_b)
        # CHECK FOR A SAME EMAIL-PREFIX
        if prefix_a in generic_prefixes or prefix_b in generic_prefixes:
            if c1 < 0.60:
                c2 = 0
            else:
                c2 = sim(prefix_a, prefix_b)
        else:
            c2 = sim(prefix_a, prefix_b)
        c31 = sim(first_a, first_b)
        c32 = sim(last_a, last_b)

        # Similarity without c4 - c7
        SIMILARITY.append([dev_a[0], email_a, dev_b[0], email_b, c1, c2, c31, c32])

    print(f"\nno_c4c7 improved, email check -> True")
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
                f"devs_similarity_no_c4c7_improved_t={t}.csv",
            ),
            index=False,
            header=True,
        )
