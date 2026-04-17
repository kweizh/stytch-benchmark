import os
import shutil
import pytest

PROJECT_DIR = "/home/user/stytch_sso"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_stytch_installed():
    try:
        import stytch
    except ImportError:
        pytest.fail("stytch module is not installed.")
