import os
import sys

def test_app_not_exists():
    assert not os.path.exists("/home/user/app.py"), "app.py should not exist initially"
