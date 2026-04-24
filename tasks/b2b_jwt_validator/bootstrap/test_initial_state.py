import os
import shutil

def test_nodejs_installed():
    assert shutil.which("node") is not None, "Node.js is not installed."
    assert shutil.which("npm") is not None, "npm is not installed."

def test_stytch_env_vars():
    assert os.environ.get("STYTCH_B2B_PROJECT_ID") is not None, "STYTCH_B2B_PROJECT_ID is not set."
    assert os.environ.get("STYTCH_B2B_SECRET") is not None, "STYTCH_B2B_SECRET is not set."

def test_app_dir_exists():
    assert os.path.exists("/home/user/app"), "/home/user/app directory does not exist."
