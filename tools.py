import unicodedata
import string
import os
import csv
from pydriller import Repository


def get_repository(repo_uri: str) -> tuple[list[list[str]], str]:
    """
    Locate a repository from its URI, collect its contributors, and ensure a data folder with
    a CSV of developers exists for that repository.

    The function derives a repository base name from the provided URI, ensures a directory
    named "{repo_name}-data" exists (creating it if necessary), and writes a "devs.csv"
    file containing the unique developers (name and email) discovered by traversing commits
    via pydriller. If the data folder already exists the function will read the existing
    "devs.csv" instead of recreating it.

    Parameters
    ----------
    repo_uri : str
        The Git repository URI (e.g. "https://github.com/user/repo.git"). The repository
        base name is extracted from the URI and used to form the data folder name.

    Returns
    -------
    tuple[list[str], str]
        A tuple where:
        - The first element is a list of developer rows read from "devs.csv".
        - The second element is the repository base name used for the data folder.
    """
    uri_tokens = repo_uri.split(sep="/")
    data_folder = uri_tokens[4].split(".git")[0] + "-data"
    devs_csv = os.path.join(f"{data_folder}", "devs.csv")

    try:
        os.mkdir(f"{data_folder}")
        DEVS = set()
        for commit in Repository(repo_uri).traverse_commits():
            DEVS.add((commit.author.name, commit.author.email))
            DEVS.add((commit.committer.name, commit.committer.email))

        DEVS = sorted(DEVS)

        with open(devs_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar='"')
            writer.writerow(["name", "email"])
            writer.writerows(DEVS)
    except FileExistsError:
        print(f"Using existing data folder: {data_folder}")

    # This block of code reads an existing csv of developers
    DEVS = []
    # Read csv file with name,dev columns
    with open(devs_csv, "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            DEVS.append(row)
    # First element is header, skip
    DEVS = DEVS[1:]

    print(f"Developers: {len(DEVS)}")

    return DEVS, data_folder


def process(dev: list[str]) -> tuple[str, str, str, str, str, str, str]:
    """
    Process developer information to extract and normalize name components and email details.

    Takes a developer tuple containing name and email, then normalizes the name by removing
    punctuation, accents, and extra whitespace. Splits the normalized name into first and
    last name components and extracts initials. Also extracts the email prefix.

    Args
    -------
    dev : list[str]
        Row from devs.csv: ["name","email"]

    Returns
    -------
    tuple[str, str, str, str, str, str, str]
        A tuple containing:
            - name: Normalized full name
            - first: First name
            - last: Last name
            - i_first: First name initial
            - i_last: Last name initial
            - email: Original email address
            - prefix: Email prefix

    """
    name: str = dev[0]

    # Remove punctuation
    trans = name.maketrans("", "", string.punctuation)
    name = name.translate(trans)
    # Remove accents, diacritics
    name = unicodedata.normalize("NFKD", name)
    name = "".join([c for c in name if not unicodedata.combining(c)])
    # Lowercase
    name = name.casefold()
    # Strip whitespace
    name = " ".join(name.split())

    # Attempt to split name into firstname, lastname by space
    parts = name.split(" ")
    # Expected case
    if len(parts) == 2:
        first, last = parts
    # If there is no space, firstname is full name, lastname empty
    elif len(parts) == 1:
        first, last = name, ""
    # If there is more than 1 space, firstname is until first space, rest is lastname
    else:
        first, last = parts[0], " ".join(parts[1:])

    # Take initials of firstname and lastname if they are long enough
    i_first = first[0] if len(first) > 1 else ""
    i_last = last[0] if len(last) > 1 else ""

    # Determine email prefix
    email: str = dev[1]
    prefix = email.split("@")[0]

    return name, first, last, i_first, i_last, email, prefix


def most_common_prefixes(devs: list[list[str]], number: int):
    """
    Finds the most common email prefixes and prints the specified number of them.

    Args
    -------
    dev : list[list[str]]
        Full list of devs from devs.csv

    number : int
        The number of prefixes to include in the print.
    """
    most_common_prefixes = {}

    for dev in devs:
        prefix = dev[1].split("@")[0]
        if prefix in most_common_prefixes.keys():
            most_common_prefixes[prefix] += 1
        else:
            most_common_prefixes[prefix] = 1

        # Get the 10 most common prefixes
    most_common_prefixes = dict(
        sorted(
            most_common_prefixes.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:number]
    )
    print("Most common prefixes in devs: ")
    longest_prefix = max(len(i) for i in most_common_prefixes) + 1
    for i in range(len(most_common_prefixes)):
        print(
            f"{str(list(most_common_prefixes.keys())[i]).rjust(longest_prefix, " ")}: {list(most_common_prefixes.values())[i]}"
        )
    print("__________________________")
