import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_app_js_exists():
    app_js_path = os.path.join(PROJECT_DIR, "app.js")
    assert os.path.isfile(app_js_path), f"{app_js_path} does not exist."

def test_package_json_exists():
    pkg_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_json_path), f"{pkg_json_path} does not exist."
