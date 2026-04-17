import os
import shutil
import pytest

PROJECT_DIR = "/home/user/stytch-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"

def test_index_js_exists():
    index_js_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_js_path), f"index.js not found at {index_js_path}"

def test_npm_available():
    assert shutil.which("npm") is not None, "npm command not found in PATH."
