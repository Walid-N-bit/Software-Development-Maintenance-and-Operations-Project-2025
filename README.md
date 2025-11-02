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

5. Run the program:

    ```bash
    python main.py
    ```
