import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/stytch_project"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_stytch_installed():
    result = subprocess.run(["python3", "-c", "import stytch"], capture_output=True)
    assert result.returncode == 0, "stytch python package is not installed."

def test_pyotp_installed():
    result = subprocess.run(["python3", "-c", "import pyotp"], capture_output=True)
    assert result.returncode == 0, "pyotp python package is not installed."
