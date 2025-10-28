from tools import get_repository

# import all evaluation functions
from evalutation import *


def main():
    repo_uri = "https://github.com/fastapi/fastapi.git"
    devs, folder_path = get_repository(repo_uri)
    # Check for generic email-prefix
    email_check = False
    # Set the threshholds to use
    threshholds = [0.5, 0.6, 0.7, 0.8, 0.9]

    # If more similarity versions, add booleans or make a new function
    # similarity_default(devs, folder_path, email_check, threshholds)
    similarity_no_c4c7(devs, folder_path, email_check, threshholds)


if __name__ == "__main__":
    main()
