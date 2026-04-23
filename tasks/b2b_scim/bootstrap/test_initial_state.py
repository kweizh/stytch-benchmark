import os
import pytest

APP_DIR = "/home/user/app"

def test_app_directory_exists():
    assert os.path.isdir(APP_DIR), f"Expected {APP_DIR} to exist."

def test_setup_scim_script_does_not_exist():
    script_path = os.path.join(APP_DIR, "setup_scim.js")
    assert not os.path.exists(script_path), f"Expected {script_path} to not exist initially."

def test_scim_output_does_not_exist():
    output_path = os.path.join(APP_DIR, "scim_output.json")
    assert not os.path.exists(output_path), f"Expected {output_path} to not exist initially."
