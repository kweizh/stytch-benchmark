import os
import subprocess

def test_node_installed():
    result = subprocess.run(["node", "-v"], capture_output=True, text=True)
    assert result.returncode == 0, "Node.js is not installed"

def test_npm_installed():
    result = subprocess.run(["npm", "-v"], capture_output=True, text=True)
    assert result.returncode == 0, "npm is not installed"

def test_project_dir_exists():
    assert os.path.exists("/home/user/app"), "Project directory /home/user/app does not exist"
