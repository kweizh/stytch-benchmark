import os
import shutil
import pytest

PROJECT_DIR = "/home/user/workspace"

def test_python3_available():
    assert shutil.which("python3") is not None, "python3 binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_stytch_b2b_credentials_exist():
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    assert project_id is not None, "STYTCH_B2B_PROJECT_ID environment variable is missing."
    assert secret is not None, "STYTCH_B2B_SECRET environment variable is missing."
