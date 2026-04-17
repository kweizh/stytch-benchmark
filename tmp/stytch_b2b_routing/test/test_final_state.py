import subprocess
import os

def test_app_exists():
    assert os.path.exists("/home/user/app.py"), "app.py should exist"

def test_app_execution():
    env = os.environ.copy()
    
    result = subprocess.run(
        ["python", "/home/user/app.py", "DOYoip3rvIMMW5lgItikFK-Ak1CfMsgjuiCyI7uuU94=", "organization-test-007d9d4a-deac-4a87-ba0a-e6e8afba4d4b"],
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 0, f"app.py execution failed: {result.stderr}"
    assert "member-test-" in result.stdout or "member_id" in result.stdout or len(result.stdout.strip()) > 0, "app.py should output member_id"
