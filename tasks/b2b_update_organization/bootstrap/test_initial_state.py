import os
import subprocess

PROJECT_DIR = "/home/user/stytch_project"

def test_stytch_package_available():
    result = subprocess.run(
        ["python3", "-c", "import stytch"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "stytch python package is not installed."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
