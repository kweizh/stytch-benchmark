import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_dependencies_installed():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    with open(package_json_path, "r") as f:
        package_data = json.load(f)
    
    dependencies = package_data.get("dependencies", {})
    assert "@stytch/nextjs" in dependencies, "@stytch/nextjs is not installed in package.json."
    assert "@stytch/vanilla-js" in dependencies, "@stytch/vanilla-js is not installed in package.json."

def test_layout_contains_provider_and_token():
    layout_path = os.path.join(PROJECT_DIR, "app", "layout.tsx")
    with open(layout_path, "r") as f:
        content = f.read()
    
    assert "StytchB2BProvider" in content, "StytchB2BProvider is not used in app/layout.tsx."
    assert "public-token-test-11111111-1111-1111-1111-111111111111" in content, \
        "The correct Stytch public token is not present in app/layout.tsx."

def test_login_page_contains_stytch_component():
    login_page_path = os.path.join(PROJECT_DIR, "app", "login", "page.tsx")
    assert os.path.isfile(login_page_path), f"File {login_page_path} does not exist."
    
    with open(login_page_path, "r") as f:
        content = f.read()
    
    assert "StytchB2B" in content, "StytchB2B component is not used in app/login/page.tsx."
    assert "AuthFlowType" in content, "AuthFlowType is not imported or used in app/login/page.tsx."
    assert "AuthFlowType.Discovery" in content, "AuthFlowType.Discovery is not configured in app/login/page.tsx."
    assert "emailMagicLinks" in content, "emailMagicLinks is not included in the products array."
    assert "http://localhost:3000/authenticate" in content, "loginRedirectURL or signupRedirectURL is not set correctly."

def test_next_build_succeeds():
    result = subprocess.run(
        ["npm", "run", "build"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'npm run build' failed: {result.stderr or result.stdout}"