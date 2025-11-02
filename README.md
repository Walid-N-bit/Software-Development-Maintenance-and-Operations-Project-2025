# Software-Development-Maintenance-and-Operations-Project-2025

## Virtual environment and dependencies

1. Create a virtual environment named `.venv`:

    ```bash
    python3 -m venv .venv
    ```

2. Activate the virtual environment:
    - macOS / Linux:

      ```bash
      source .venv/bin/activate
      ```

    - Windows:

      ```powershell
      .venv\Scripts\Activate
      ```

3. Install the project in editable mode (includes all dependencies from `requirements.txt`):

    ```bash
    pip install -e .
    ```

4. Run tests (optional):

    ```bash
    pytest --cov=. --cov-config=.coveragerc
    ```

    Coverage configuration file `.coveragerc` excludes `main` functions as their only purpose is to supply values and call other functions.

## Running the Program
1. **Edit variables in main()**

You can add a url for the target repository, generic email prefixes and the option to ignore them when forming developer pairs. You can also add threshold values to the list `thresholds` and set the number of common prefixes will print on console when you run the program using `most_common_prefixes()`. 

```python
    repo_uri = ""
    devs, folder_path = get_repository(repo_uri)

    # Check for generic email-prefix
    email_check = True
    generic_prefixes = {"github", "mail"}
    # Set the thresholds to use
    thresholds = [0.7, 0.8, 0.9]

    # print the 10 most common email prefixes
    most_common_prefixes(devs, 10)
```

A different csv file will be created for each threshold value and similarity function. You can skip functions by commenting them out. An output directory will be created for every repo's data.

2. **Run the program**

```bash
python main.py
```

4. **Annotate and Combine**

After necessary csv files, you may annotate them manually by assigning 1 to `true_pos` column for pairs that represent a True Positive.

In order to pass-on annotated values from one file to another for the sake of comparison using `combine_same_rows.py` module. But the file that would be annotated this way MUST be smaller. That is to say, the rows of the new file must be a subset of the rows of the original file.

You can edit the original file path, new file path and output directory in `main()` of `combine_same_rows.py`.

```python
# main annotated, the largest one
annotated_file = ""
# new, more strict, smaller one wihtout annotations
file_to_annotate = ""
# Directory to put annotated files in
annotated_dir = "annotated"
```

Then you can run:

```bash
python tools/combine_same_rows.py 
```

3. **Compute TP, FP, TP/FP, TP/(TP+FP)**

`true_positive.py` will calculate TP, FP, TP/FP, TP/(TP+FP) values for each file in the `annotated`directory.

Run with:

```bash
python tools/true_positive.py
```

