#!/usr/bin/env python3
"""
Re-encode existing student faces using OpenCV features
"""

from models.database_manager import DatabaseManager
from models.face_recognition_model import FaceRecognition
import os

def reencode_faces():
    print("Re-encoding existing student faces...")

    db = DatabaseManager()
    face_recog = FaceRecognition()

    students = db.get_all_students()
    print(f"Found {len(students)} students")

    for student in students:
        if student['image_path'] and os.path.exists(student['image_path']):
            print(f"Re-encoding face for {student['full_name']} ({student['roll_number']})")

            # Re-encode the face
            success = face_recog.register_student_face(student['roll_number'], student['image_path'])

            if success:
                print(f"✓ Successfully re-encoded {student['full_name']}")
            else:
                print(f"✗ Failed to re-encode {student['full_name']}")
        else:
            print(f"✗ No image found for {student['full_name']}")

    print("Re-encoding completed!")

if __name__ == "__main__":
    reencode_faces()