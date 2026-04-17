import os
import sys
import time
import subprocess
import urllib.request
import urllib.error

def main():
    app_dir = "/home/user/app"
    server_file = os.path.join(app_dir, "server.js")
    
    if not os.path.exists(server_file):
        print(f"Error: {server_file} does not exist.")
        sys.exit(1)
        
    with open(server_file, "r") as f:
        content = f.read()
        
    if "authenticateJwtLocal" in content:
        print("Error: The server.js still uses authenticateJwtLocal. It should use authenticate to immediately catch revoked sessions.")
        sys.exit(1)
        
    if "authenticate(" not in content:
        print("Error: The server.js does not use client.sessions.authenticate().")
        sys.exit(1)
        
    # Start the server to ensure no syntax errors
    process = subprocess.Popen(["node", "server.js"], cwd=app_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3) # Wait for server to start
    
    if process.poll() is not None:
        print("Error: The server failed to start.")
        stdout, stderr = process.communicate()
        print(stderr.decode())
        sys.exit(1)
        
    try:
        req = urllib.request.Request(
            "http://localhost:3000/protected",
            headers={"Authorization": "Bearer invalid_token"}
        )
        try:
            response = urllib.request.urlopen(req)
            print(f"Error: Expected 401 Unauthorized for invalid token, got {response.status}")
            process.terminate()
            sys.exit(1)
        except urllib.error.HTTPError as e:
            if e.code != 401:
                print(f"Error: Expected 401 Unauthorized for invalid token, got {e.code}")
                process.terminate()
                sys.exit(1)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        process.terminate()
        sys.exit(1)
        
    process.terminate()
    print("Final state verification passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
