from tools.helpers import get_repository, most_common_prefixes

# import all evaluation functions
from evaluators.similarity_default import similarity_default
from evaluators.similarity_jaro import similarity_jw_bird
from evaluators.similarity_no_c4c7 import similarity_no_c4c7
from evaluators.similarity_no_c4c7_improved import similarity_no_c4c7_email_improved


def main():
    repo_uri = ""
    devs, folder_path = get_repository(repo_uri)

    # Check for generic email-prefix
    email_check = True
    generic_prefixes = {
        "mail",
        "github",
        "git",
        "info",
        "hello",
        "me",
        "contact",
        "dev",
        "support",
        "admin",
    }
    # Set the thresholds to use
    thresholds = [0.9, 0.99]

    # print the 10 most common email prefixes
    most_common_prefixes(devs, 10)

    # If more similarity versions, add booleans or make a new function
    # similarity_default(devs, folder_path, email_check, generic_prefixes, thresholds)
    similarity_no_c4c7(devs, folder_path, email_check, generic_prefixes, thresholds)
    # similarity_jw_bird(devs, folder_path, email_check, generic_prefixes, thresholds)
    similarity_no_c4c7_email_improved(devs, folder_path, generic_prefixes, thresholds)


if __name__ == "__main__":
    main()
