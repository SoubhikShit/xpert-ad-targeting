#!/usr/bin/env python3
"""
Installation script for XPERT AD-TARGETING package.
This script installs the package in development mode for easy testing.
"""

import subprocess
import sys
import os

def install_package():
    """Install the package in development mode"""
    print("Installing XPERT AD-TARGETING package in development mode...")
    
    try:
        # Install in development mode
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✅ Package installed successfully!")
        
        # Show usage instructions
        print("\n" + "="*50)
        print("INSTALLATION COMPLETE!")
        print("="*50)
        print("\nYou can now run the application in several ways:")
        print("\n1. Using the command line:")
        print("   xpert-ad-targeting")
        print("\n2. Using Python module:")
        print("   python -m Project_Xpert")
        print("\n3. Using Python directly:")
        print("   python -c \"from Project_Xpert import run; run()\"")
        print("\n4. From your code:")
        print("   from Project_Xpert import XpertPOSApp")
        print("   app = XpertPOSApp()")
        print("   app.window.mainloop()")
        print("\n" + "="*50)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_package() 