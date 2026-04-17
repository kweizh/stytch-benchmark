import os
import shutil
import pytest

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_stytch_env_vars_available():
    assert "STYTCH_PROJECT_ID" in os.environ, "STYTCH_PROJECT_ID environment variable is missing."
    assert "STYTCH_SECRET" in os.environ, "STYTCH_SECRET environment variable is missing."
