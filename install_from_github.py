#!/usr/bin/env python3
"""
Standalone installation script for XPERT AD-TARGETING from GitHub.
This script can be downloaded and run to install the package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("XPERT AD-TARGETING - GitHub Installation")
    print("=" * 60)
    
    # Check if git is available
    if not shutil.which("git"):
        print("❌ Git is not installed or not in PATH.")
        print("Please install Git from: https://git-scm.com/")
        return 1
    
    # Get repository URL from user
    print("📝 Please provide your GitHub repository URL:")
    print("   Example: https://github.com/yourusername/xpert-ad-targeting.git")
    repo_url = input("Repository URL: ").strip()
    
    if not repo_url:
        print("❌ Repository URL is required.")
        return 1
    
    # Create installation directory
    install_dir = Path.cwd() / "xpert-ad-targeting"
    if install_dir.exists():
        response = input(f"⚠️  Directory {install_dir} already exists. Remove it? (y/N): ").strip().lower()
        if response == 'y':
            shutil.rmtree(install_dir)
        else:
            print("Installation cancelled.")
            return 0
    
    # Clone the repository
    if not run_command(f"git clone {repo_url} {install_dir}", "Cloning repository"):
        return 1
    
    # Change to the installation directory
    os.chdir(install_dir)
    
    # Install the package
    if not run_command("pip install -e .", "Installing package"):
        return 1
    
    # Set up environment
    print("🔄 Setting up environment configuration...")
    if Path("setup_env.py").exists():
        if not run_command("python setup_env.py", "Setting up environment"):
            print("⚠️  Environment setup failed, but installation completed.")
    else:
        print("⚠️  setup_env.py not found. Please manually copy env.example to .env")
    
    print("\n" + "=" * 60)
    print("🎉 Installation completed successfully!")
    print("=" * 60)
    print()
    print("📝 Next steps:")
    print("1. Configure your environment variables:")
    print(f"   - Edit the .env file in: {install_dir}")
    print("   - Add your AWS and MongoDB credentials")
    print()
    print("2. Run the application:")
    print("   xpert-ad-targeting")
    print()
    print("📚 For more information, see the README.md file")
    print("🔒 Remember: Never commit your .env file to version control!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 