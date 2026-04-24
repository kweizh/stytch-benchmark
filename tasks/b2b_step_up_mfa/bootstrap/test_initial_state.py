import os
import subprocess
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_server_js_exists():
    server_js_path = os.path.join(PROJECT_DIR, "server.js")
    assert os.path.isfile(server_js_path), f"File {server_js_path} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"File {package_json_path} does not exist."
