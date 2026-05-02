#!/usr/bin/env python3
"""
Quick test script for the face detection attendance system
"""

from models.database_manager import DatabaseManager
from models.face_recognition_model import FaceRecognition

def test_system():
    print("Testing Face Detection Attendance System...")

    # Test database
    try:
        db = DatabaseManager()
        print("✓ Database manager initialized")
    except Exception as e:
        print(f"✗ Database error: {e}")
        return

    # Test face recognition
    try:
        face_recog = FaceRecognition()
        print("✓ Face recognition model initialized")
        print(f"  - Known faces loaded: {len(face_recog.known_face_features)}")
        print(f"  - Face recognition available: {face_recog.__class__.__module__ == 'models.face_recognition_model'}")
    except Exception as e:
        print(f"✗ Face recognition error: {e}")
        return

    print("✓ System test completed successfully!")

if __name__ == "__main__":
    test_system()