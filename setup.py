"""
Setup script to prepare the Face Detection Attendance System
"""

import os
import subprocess
import sys

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ['faces', 'data']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"  Directory already exists: {directory}")

def main():
    """Main setup function"""
    print("="*60)
    print("Face Detection Attendance System - Setup")
    print("="*60)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup incomplete. Please install dependencies manually:")
        print("  pip install -r requirements.txt")
        return
    
    print("\n" + "="*60)
    print("Setup completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Register faces: python register_face.py")
    print("2. Run attendance system: python attendance_system.py")
    print("3. View attendance: python view_attendance.py")
    print("="*60)

if __name__ == "__main__":
    main()
