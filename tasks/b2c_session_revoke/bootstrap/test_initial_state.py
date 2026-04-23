import os
import pytest
import json

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json not found at {pkg_path}"
    with open(pkg_path) as f:
        data = json.load(f)
    assert "express" in data.get("dependencies", {}), "express dependency missing"
    assert "stytch" in data.get("dependencies", {}), "stytch dependency missing"

def test_index_js_exists():
    index_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_path), f"index.js not found at {index_path}"
    with open(index_path) as f:
        content = f.read()
    assert "const revokedSessions = new Set();" in content, "revokedSessions Set not found in index.js"
    assert "app.post('/logout'" in content, "/logout endpoint missing in index.js"
    assert "app.get('/profile'" in content, "/profile endpoint missing in index.js"
