import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_stytch_installed():
    try:
        subprocess.run(["python", "-c", "import stytch"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pytest.fail("The 'stytch' python package is not installed.")
