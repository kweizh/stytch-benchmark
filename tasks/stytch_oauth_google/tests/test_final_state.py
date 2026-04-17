import os
import ast
import pytest

PROJECT_DIR = "/home/user/myproject"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "authenticate.py")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_script_logic():
    with open(SCRIPT_PATH, "r") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in authenticate.py: {e}")

    # Check for imports
    imports_stytch = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "stytch":
                    imports_stytch = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == "stytch":
                imports_stytch = True

    assert imports_stytch, "The script does not import the 'stytch' module."

    # Check if 'oauth.authenticate' is called
    calls_authenticate = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check if it's a method call like client.oauth.authenticate
            if isinstance(node.func, ast.Attribute) and node.func.attr == "authenticate":
                # It might be client.oauth.authenticate
                if isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "oauth":
                    calls_authenticate = True

    assert calls_authenticate, "The script does not call 'client.oauth.authenticate'."

    # Check if os.environ is accessed for STYTCH_PROJECT_ID and STYTCH_SECRET
    accesses_project_id = "STYTCH_PROJECT_ID" in source
    accesses_secret = "STYTCH_SECRET" in source
    assert accesses_project_id, "The script does not seem to read STYTCH_PROJECT_ID from the environment."
    assert accesses_secret, "The script does not seem to read STYTCH_SECRET from the environment."
