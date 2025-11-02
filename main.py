from tools import get_repository

# import all evaluation functions
from evalutation import (
    similarity_default,
    similarity_no_c4c7,
    similarity_modified_bird,
    similarity_no_c4c7_email_improved,
)


def main():
    repo_uri = ""
    devs, folder_path = get_repository(repo_uri)

    # Check for generic email-prefix
    email_check = True
    generic_prefixes = {"mail", "github", "git", "info", "hello", "me"}
    # Set the thresholds to use
    thresholds = [0.9, 0.99]

    # If more similarity versions, add booleans or make a new function
    # similarity_default(devs, folder_path, email_check, generic_prefixes, thresholds)
    similarity_no_c4c7(devs, folder_path, email_check, generic_prefixes, thresholds)
    # similarity_modified_bird(
    #     devs, folder_path, email_check, generic_prefixes, thresholds
    # )
    similarity_no_c4c7_email_improved(devs, folder_path, generic_prefixes, thresholds)


if __name__ == "__main__":
    main()
