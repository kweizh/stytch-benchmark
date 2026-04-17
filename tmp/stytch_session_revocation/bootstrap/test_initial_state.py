import os
import sys

def main():
    app_dir = "/home/user/app"
    server_file = os.path.join(app_dir, "server.js")
    
    if not os.path.exists(server_file):
        print(f"Error: {server_file} does not exist.")
        sys.exit(1)
        
    with open(server_file, "r") as f:
        content = f.read()
        
    if "authenticateJwtLocal" not in content:
        print("Error: The initial server.js must use authenticateJwtLocal.")
        sys.exit(1)
        
    print("Initial state verification passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
