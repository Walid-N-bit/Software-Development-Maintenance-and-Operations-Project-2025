import pytest
import os
from shutil import rmtree
from tools.helpers import process, most_common_prefixes, get_repository
from tools.true_positive import calc_tp
from tools.combine_same_rows import annotate


def test_process_normal_name():
    dev = ["John Doe", "john.doe@example.com"]
    name, first, last, i_first, i_last, email, prefix = process(dev)

    assert name == "john doe"
    assert first == "john"
    assert last == "doe"
    assert i_first == "j"
    assert i_last == "d"
    assert email == "john.doe@example.com"
    assert prefix == "john.doe"


def test_process_single_name():
    dev = ["house", "house@med.us"]
    name, first, last, i_first, i_last, email, prefix = process(dev)

    assert name == "house"
    assert first == "house"
    assert last == ""
    assert i_first == "h"
    assert i_last == ""
    assert email == "house@med.us"
    assert prefix == "house"


def test_process_two_spaces():
    dev = ["Mr Test driver", "mrtestdriver@example.com"]
    name, first, last, i_first, i_last, email, prefix = process(dev)

    assert name == "mr test driver"
    assert first == "mr"
    assert last == "test driver"
    assert i_first == "m"
    assert i_last == "t"
    assert email == "mrtestdriver@example.com"
    assert prefix == "mrtestdriver"


def test_most_common_prefixes_prints_top(capsys):
    devs = [
        ["A", "alpha@example.com"],
        ["B", "bravo@x.com"],
        ["C", "bravo@example.com"],
        ["D", "delta@ex.com"],
        ["E", "echo@test.com"],
        ["F", "echo@outlook.com"],
        ["G", "bravo@again.com"],
    ]

    # get top 2 prefix
    most_common_prefixes(devs, 2)
    captured = capsys.readouterr()

    # should have 3 bravo 2 echo
    assert "bravo" in captured.out
    assert ": 3" in captured.out
    assert "echo" in captured.out
    assert ": 2" in captured.out


def test_repo():
    """Test repository mining, uses the actual implementation."""
    # use this repository as a test also should have static results
    repo_uri = "https://github.com/Walid-N-bit/Software-Development-Maintenance-and-Operations-Project-2025.git"
    devs, datafolder = get_repository(repo_uri)

    assert devs[1] == ["Matias Paavilainen", "matias.paavilainen@gmail.com"]
    assert (
        datafolder
        == "Software-Development-Maintenance-and-Operations-Project-2025-data"
    )
    assert os.path.isdir(datafolder)
    devs_csv = os.path.join(datafolder, "devs.csv")
    assert os.path.isfile(devs_csv)
    with open(devs_csv, "r") as file:
        lines = file.readlines()
        assert len(lines) > 0
        assert lines[1] == "GitHub,noreply@github.com\n"


def test_repo_folder_exists(capsys):
    """Test repository mining, when the datafolder already exists."""
    repo_uri = "https://github.com/Walid-N-bit/Software-Development-Maintenance-and-Operations-Project-2025.git"
    _, datafolder = get_repository(repo_uri)

    captured = capsys.readouterr()
    assert f"Using existing data folder: {datafolder}" in captured.out

    rmtree(datafolder)


def test_true_positive_calc():
    """Test TP, folder contains 1 valid and 1 invalid file."""
    path = "tests/csvs"
    result = calc_tp(path)
    print(result)

    assert len(result) == 5
    # test if the invalid file is skipped
    assert result[0] == None
    # test the calculation
    assert result[4] == "P: 6, TP: 3, FP: 3, Ratio: 1.00, File: test_annotated.csv"


def test_combine_rows_correct_files():
    """Test that annotate succeeds when new file is subset of annotated file."""
    annotate(
        "tests/csvs/test_annotated.csv",
        "tests/csvs/test_new_with_less.csv",
        "tests/annotated_test_dir",
    )
    # If no exception is raised, test passes


def test_combine_rows_new_file_longer():
    """Test that annotate raises ValueError when new file is longer."""
    with pytest.raises(ValueError, match="New File is longer!"):
        annotate(
            "tests/csvs/test_annotated.csv",
            "tests/csvs/test_new_with_more.csv",
            "tests/annotated_test_dir",
        )


def test_combine_rows_new_file_has_unique_data():
    """Test that annotate raises ValueError when new file contains unique rows."""
    # Create temp files where new file has a row not in annotated file
    with pytest.raises(ValueError, match="New File contains unique data!"):
        annotate(
            "tests/csvs/test_annotated.csv",
            "tests/csvs/test_new_with_unique.csv",
            "tests/annotated_test_dir",
        )


def test_combine_rows_create_new_dir():
    """Test that the specified directory is created if missing."""
    rmtree("tests/annotated_test_dir")
    annotate(
        "tests/csvs/test_annotated.csv",
        "tests/csvs/test_new_with_less.csv",
        "tests/annotated_test_dir",
    )

    assert os.path.isdir("tests/annotated_test_dir")
