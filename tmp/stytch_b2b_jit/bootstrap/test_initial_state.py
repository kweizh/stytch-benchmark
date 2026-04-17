import os
import shutil
import pytest
import json

PROJECT_DIR = "/home/user/project"

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_stytch_package_installed():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found in {PROJECT_DIR}."
    with open(package_json_path) as f:
        pkg = json.load(f)
    deps = pkg.get("dependencies", {})
    assert "stytch" in deps, "The 'stytch' package is not installed in the project."
