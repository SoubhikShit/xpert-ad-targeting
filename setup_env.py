#!/usr/bin/env python3
"""
Setup script for XPERT AD-TARGETING environment configuration.
This script helps users create their .env file after installation.
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("XPERT AD-TARGETING - Environment Setup")
    print("=" * 60)
    
    # Get the current directory
    current_dir = Path.cwd()
    env_example = current_dir / "env.example"
    env_file = current_dir / ".env"
    
    # Check if we're in the right directory
    if not env_example.exists():
        print("❌ Error: env.example file not found!")
        print("Please run this script from the directory where you installed xpert-ad-targeting.")
        print(f"Current directory: {current_dir}")
        return 1
    
    # Check if .env already exists
    if env_file.exists():
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return 0
    
    try:
        # Copy env.example to .env
        shutil.copy2(env_example, env_file)
        print("✅ Successfully created .env file!")
        print(f"📁 Location: {env_file}")
        print()
        print("📝 Next steps:")
        print("1. Edit the .env file with your actual credentials:")
        print(f"   - Open: {env_file}")
        print("   - Replace placeholder values with your real credentials")
        print()
        print("2. Required configuration:")
        print("   - AWS_ACCESS_KEY_ID: Your AWS access key")
        print("   - AWS_SECRET_ACCESS_KEY: Your AWS secret key")
        print("   - AWS_REGION: Your AWS region (e.g., ap-south-1)")
        print("   - S3_BUCKET_NAME: Your S3 bucket name")
        print("   - MONGO_URI: Your MongoDB connection string")
        print()
        print("3. Run the application:")
        print("   xpert-ad-targeting")
        print()
        print("🔒 Security Note: Never commit your .env file to version control!")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 