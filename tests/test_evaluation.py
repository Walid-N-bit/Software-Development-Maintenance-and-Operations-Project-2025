import os
from shutil import rmtree

from evaluators.similarity_default import (
    bird_c1_c3,
    bird_c4_c7,
    similarity_default,
)

from evaluators.similarity_jaro import similarity_jw_bird, jaro_c1_c4
from evaluators.similarity_no_c4c7 import similarity_no_c4c7
from evaluators.similarity_no_c4c7_improved import similarity_no_c4c7_email_improved

from tools.helpers import get_repository

DEV_A = ["John Doe", "john.doe@example.com"]
DEV_B = ["Jane Doe", "jane.doe@example.com"]
DEV_A_GEN = ["John Doe", "github@example.com"]
DEV_B_NOT_SAME_INIT = ["Mark Twain", "marktwain@gmail.com"]
GENERIC_PREFIXES = {"github"}

DEVS, DATAFOLDER = get_repository(
    "https://github.com/Walid-N-bit/Software-Development-Maintenance-and-Operations-Project-2025.git"
)
THRESHOLDS = [0.8]


def teardown_module():
    rmtree(DATAFOLDER)


def test_bird_c1_c3_no_email():
    result = bird_c1_c3(DEV_A, DEV_B, GENERIC_PREFIXES, False)

    assert isinstance(result[0], float)
    assert isinstance(result[1], float)
    assert isinstance(result[2], float)
    # same last name
    assert result[3] == 1
    assert result[4] == "john.doe@example.com"
    assert result[5] == "jane.doe@example.com"


def test_bird_ci_c3_no_email_same_person():
    result = bird_c1_c3(DEV_A, DEV_A, GENERIC_PREFIXES, False)

    assert result[0] == 1
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == 1
    assert result[4] == "john.doe@example.com"
    assert result[5] == "john.doe@example.com"


def test_bird_c1_c3_email_check():
    result = bird_c1_c3(DEV_A, DEV_A_GEN, GENERIC_PREFIXES, True)

    assert result[0] == 1
    # Check that c2 is 0 when prefix in generic
    assert result[1] == 0
    assert result[2] == 1
    assert result[3] == 1
    assert result[4] == "john.doe@example.com"
    assert result[5] == "github@example.com"


def test_bird_c4_c7_same_initials():
    result = bird_c4_c7(DEV_A, DEV_B)

    assert result[0] == True
    assert result[1] == False
    assert result[2] == True
    assert result[3] == False


def test_bird_c4_c7_diff_init():
    result = bird_c4_c7(DEV_A, DEV_B_NOT_SAME_INIT)

    assert result[0] == False
    assert result[1] == False
    assert result[2] == False
    assert result[3] == False


def test_default_sim(capsys):
    similarity_default(DEVS, DATAFOLDER, False, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(DATAFOLDER, f"devs_similarity_t={THRESHOLDS[0]}.csv")
    )


def test_default_sim_email(capsys):
    similarity_default(DEVS, DATAFOLDER, True, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_similarity_email_check={len(GENERIC_PREFIXES)}_t={THRESHOLDS[0]}.csv",
        )
    )


def test_sim_no_c4_c7(capsys):
    similarity_no_c4c7(DEVS, DATAFOLDER, False, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(DATAFOLDER, f"devs_similarity_no_c4c7_t={THRESHOLDS[0]}.csv")
    )


def test_sim_no_c4_c7_email(capsys):
    similarity_no_c4c7(DEVS, DATAFOLDER, True, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_similarity_no_c4c7_email_check={len(GENERIC_PREFIXES)}_t={THRESHOLDS[0]}.csv",
        )
    )


def test_c1_c4_jaro():
    result = jaro_c1_c4(DEV_A, DEV_B, GENERIC_PREFIXES, False)

    assert isinstance(result[0], float)
    assert isinstance(result[1], float)
    # Same first initial and last name
    assert result[2] == 1

    assert result[4] == "john.doe@example.com"
    assert result[5] == "jane.doe@example.com"


def test_c1_c4_jaro_email():
    result = jaro_c1_c4(DEV_A, DEV_A_GEN, GENERIC_PREFIXES, True)

    assert isinstance(result[0], float)
    assert result[1] == 0
    # Same first initial and last name
    assert result[2] == 1

    assert result[4] == "john.doe@example.com"
    assert result[5] == "github@example.com"


def test_sim_jaro_no_email(capsys):
    similarity_jw_bird(DEVS, DATAFOLDER, False, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_jw_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_jw_similarity_t={THRESHOLDS[0]}.csv",
        )
    )


def test_sim_jaro_email(capsys):
    similarity_jw_bird(DEVS, DATAFOLDER, True, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_jw_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_jw_similarity_email_check={len(GENERIC_PREFIXES)}_t={THRESHOLDS[0]}.csv",
        )
    )


def test_sim_c4c7_improved(capsys):
    similarity_no_c4c7_email_improved(DEVS, DATAFOLDER, GENERIC_PREFIXES, THRESHOLDS)

    captured = capsys.readouterr()

    assert "Pairs: 6" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_similarity_no_c4c7_improved_t={THRESHOLDS[0]}.csv",
        )
    )


def test_sim_c4c7_improved_generic_c2is0(capsys):
    """When two devs have generic email, and names are different."""
    similarity_no_c4c7_email_improved(
        [["Mark Twain", "github@gmail.com"], ["John Doe", "github@gmail.com"]],
        DATAFOLDER,
        GENERIC_PREFIXES,
        THRESHOLDS,
    )

    captured = capsys.readouterr()
    print(captured.out)
    assert "Pairs: 1" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_similarity_no_c4c7_improved_t={THRESHOLDS[0]}.csv",
        )
    )


def test_sim_c4c7_improved_generic_c2not0(capsys):
    """When two devs have generic email, and names are similar."""
    similarity_no_c4c7_email_improved(
        [["Jane Doe", "github@gmail.com"], ["John Doe", "github@gmail.com"]],
        DATAFOLDER,
        GENERIC_PREFIXES,
        THRESHOLDS,
    )

    captured = capsys.readouterr()
    print(captured.out)
    assert "Pairs: 1" in captured.out
    assert f"Threshold: {THRESHOLDS[0]}" in captured.out
    assert os.path.isfile(os.path.join(DATAFOLDER, "devs_similarity.csv"))
    assert os.path.isfile(
        os.path.join(
            DATAFOLDER,
            f"devs_similarity_no_c4c7_improved_t={THRESHOLDS[0]}.csv",
        )
    )
