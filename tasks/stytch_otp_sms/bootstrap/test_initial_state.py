import os
import shutil
import pytest

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_installed():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_stytch_app_dir_exists():
    assert os.path.isdir("/home/user/stytch_app"), "/home/user/stytch_app directory does not exist."
