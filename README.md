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

3. Install dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. Run tests:

    ```bash
    pytest --cov=. --cov-config=.coveragerc
    ```

    Coverage configuration file .coveragerc, main functions have been ignored as their only purpose is to supply values and call other functions, nothing of interest happens in them.
