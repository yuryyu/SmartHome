#!/usr/bin/env python3
"""
Setup script for Google Cloud credentials in SmartHome project.
Supports both environment variable and local file approaches.
"""

import os
import sys
import json
from pathlib import Path

def setup_credentials():
    """Interactive setup for Google Cloud credentials."""
    
    print("=" * 60)
    print("SmartHome Google Cloud Credentials Setup")
    print("=" * 60)
    
    # Check if GOOGLE_APPLICATION_CREDENTIALS is already set
    existing_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if existing_path and os.path.exists(existing_path):
        print(f"\n✓ Credentials already configured at:")
        print(f"  {existing_path}")
        return
    
    print("\nChoose setup method:")
    print("1. Use environment variable (recommended for development)")
    print("2. Store in project directory (credentials/google-cloud-key.json)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        setup_environment_variable()
    elif choice == "2":
        setup_local_directory()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

def setup_environment_variable():
    """Setup credentials using environment variable."""
    print("\n" + "=" * 60)
    print("Environment Variable Setup")
    print("=" * 60)
    
    cred_path = input("\nEnter full path to your Google Cloud JSON key: ").strip()
    
    # Remove quotes if user added them
    cred_path = cred_path.strip('"').strip("'")
    
    if not os.path.exists(cred_path):
        print(f"✗ Error: File not found at {cred_path}")
        sys.exit(1)
    
    # Validate JSON
    try:
        with open(cred_path, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        print("✗ Error: File is not valid JSON")
        sys.exit(1)
    
    print("\nAdd this to your shell profile (~/.zshrc, ~/.bashrc, etc.):")
    print(f"\nexport GOOGLE_APPLICATION_CREDENTIALS=\"{cred_path}\"\n")
    
    print("Or run before starting the bot:")
    print(f"export GOOGLE_APPLICATION_CREDENTIALS=\"{cred_path}\"")
    print("python assistant_BOT.py\n")
    
    # Offer to set it temporarily for this session
    if input("Set for current session? (y/n): ").lower() == 'y':
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
        print(f"✓ Credentials set for current session")
        print(f"  Path: {cred_path}")

def setup_local_directory():
    """Setup credentials in project directory."""
    print("\n" + "=" * 60)
    print("Local Directory Setup")
    print("=" * 60)
    
    cred_path = input("\nEnter full path to your Google Cloud JSON key: ").strip()
    cred_path = cred_path.strip('"').strip("'")
    
    if not os.path.exists(cred_path):
        print(f"✗ Error: File not found at {cred_path}")
        sys.exit(1)
    
    # Create credentials directory
    project_root = Path(__file__).parent
    creds_dir = project_root / 'credentials'
    creds_dir.mkdir(exist_ok=True)
    
    target_path = creds_dir / 'google-cloud-key.json'
    
    # Copy file
    try:
        import shutil
        shutil.copy(cred_path, target_path)
        print(f"\n✓ Credentials copied to: {target_path}")
    except Exception as e:
        print(f"✗ Error copying file: {e}")
        sys.exit(1)
    
    # Create .gitignore entry
    gitignore_path = project_root / '.gitignore'
    gitignore_entries = ['credentials/', '*.json']
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            existing = f.read()
    else:
        existing = ""
    
    needs_update = False
    for entry in gitignore_entries:
        if entry not in existing:
            existing += f"\n{entry}"
            needs_update = True
    
    if needs_update:
        with open(gitignore_path, 'w') as f:
            f.write(existing.lstrip())
        print(f"✓ Updated .gitignore to exclude credentials")
    
    print("\nYour credentials are now stored locally.")
    print("Make sure .gitignore includes 'credentials/' to prevent accidental commits.\n")

if __name__ == '__main__':
    setup_credentials()
