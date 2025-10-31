from tools import get_repository

# import all evaluation functions
from evalutation import *


def main():
    repo_uri = ""
    devs, folder_path = get_repository(repo_uri)

    # Check for generic email-prefix
    email_check = True
    prefix_to_ignore = {"mail", "github", "git", "info"}
    # Set the thresholds to use
    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]

    # If more similarity versions, add booleans or make a new function
    # similarity_default(devs, folder_path, email_check, generic_prefixes, thresholds)
    # similarity_no_c4c7(devs, folder_path, email_check, prefix_to_ignore, thresholds)
    similarity_modified_bird(devs, folder_path, prefix_to_ignore, thresholds)


if __name__ == "__main__":
    main()
