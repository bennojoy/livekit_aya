#!/usr/bin/env python3
import os
import platform
import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e}")
        return False

def install_dependencies():
    system = platform.system().lower()
    
    # Check if Node.js is installed
    if not run_command("node --version"):
        print("Node.js is not installed. Installing Node.js...")
        if system == "darwin":  # macOS
            if not run_command("brew --version"):
                print("Installing Homebrew...")
                run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            run_command("brew install node")
        elif system == "linux":
            if "ubuntu" in platform.platform().lower():
                run_command("curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -")
                run_command("sudo apt-get install -y nodejs")
            else:
                print("Unsupported Linux distribution. Please install Node.js manually.")
                return False
    
    # Check if npm is installed
    if not run_command("npm --version"):
        print("npm is not installed. Please install Node.js which includes npm.")
        return False

    # Install Python dependencies
    print("Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Error installing Python dependencies.")
        return False

    # Setup Next.js project
    print("Setting up Next.js project...")
    os.chdir("aya")
    
    # Install npm dependencies
    if not run_command("npm install"):
        print("Error installing npm dependencies.")
        return False

    # Create .env.local file if it doesn't exist
    if not os.path.exists(".env.local"):
        print("Creating .env.local file...")
        with open(".env.local", "w") as f:
            f.write("""# LiveKit configuration
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
NEXT_PUBLIC_LIVEKIT_API_KEY=devkey
NEXT_PUBLIC_LIVEKIT_API_SECRET=secret
""")
    
    os.chdir("..")
    return True

def main():
    print("Starting setup...")
    if install_dependencies():
        print("\nSetup completed successfully!")
        print("\nTo start the application:")
        print("1. Start the LiveKit server")
        print("2. Run 'python livekit_agent_english.py' in one terminal")
        print("3. Run 'cd aya && npm run dev' in another terminal")
        print("4. Open http://localhost:3000 in your browser")
    else:
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 