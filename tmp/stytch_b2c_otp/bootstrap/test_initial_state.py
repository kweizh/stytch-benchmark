import os
import shutil
import pytest

PROJECT_DIR = "/home/user/stytch-b2c-otp"

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_stytch_installed():
    node_modules_dir = os.path.join(PROJECT_DIR, "node_modules", "stytch")
    assert os.path.isdir(node_modules_dir), "stytch module is not installed in the project."
