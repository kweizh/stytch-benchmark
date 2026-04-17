import os
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"File {package_json_path} does not exist."

def test_app_layout_exists():
    layout_path = os.path.join(PROJECT_DIR, "app", "layout.tsx")
    assert os.path.isfile(layout_path), f"File {layout_path} does not exist."