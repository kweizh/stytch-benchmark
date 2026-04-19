import os
import ast
import pytest

SCRIPT_PATH = "/home/user/stytch_sso/create_saml.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_stytch_imported():
    with open(SCRIPT_PATH, "r") as f:
        tree = ast.parse(f.read())
    
    imported = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "stytch":
                    imported = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == "stytch":
                imported = True
                
    assert imported, "The script does not import the 'stytch' module."

def test_b2b_client_initialized():
    with open(SCRIPT_PATH, "r") as f:
        tree = ast.parse(f.read())
        
    client_init_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check for stytch.B2BClient(...)
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "B2BClient":
                    # Check arguments
                    has_project_id = False
                    has_secret = False
                    for kw in node.keywords:
                        if kw.arg == "project_id" and getattr(kw.value, "value", getattr(kw.value, "s", None)) == "project-test-123":
                            has_project_id = True
                        if kw.arg == "secret" and getattr(kw.value, "value", getattr(kw.value, "s", None)) == "secret-test-456":
                            has_secret = True
                    
                    if has_project_id and has_secret:
                        client_init_found = True
                        
    assert client_init_found, "The script does not initialize stytch.B2BClient with the correct project_id and secret."

def test_create_connection_called():
    with open(SCRIPT_PATH, "r") as f:
        tree = ast.parse(f.read())
        
    create_connection_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check for create_connection(...)
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "create_connection":
                    has_org_id = False
                    has_display_name = False
                    has_idp = False
                    for kw in node.keywords:
                        if kw.arg == "organization_id" and getattr(kw.value, "value", getattr(kw.value, "s", None)) == "org-123":
                            has_org_id = True
                        if kw.arg == "display_name" and getattr(kw.value, "value", getattr(kw.value, "s", None)) == "Acme SAML":
                            has_display_name = True
                        if kw.arg == "identity_provider" and getattr(kw.value, "value", getattr(kw.value, "s", None)) == "okta":
                            has_idp = True
                    
                    if has_org_id and has_display_name and has_idp:
                        create_connection_found = True
                        
    assert create_connection_found, "The script does not call create_connection with the correct organization_id, display_name, and identity_provider."

def test_print_connection_id():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
        
    assert "print(" in content and "connection_id" in content, "The script does not appear to print the connection_id."
