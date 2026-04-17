import os
import shutil
import pytest

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_directory_exists():
    project_dir = "/home/user/stytch-app"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist."
