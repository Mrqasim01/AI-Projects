"""
Real-time Face Detection Attendance System
Detects faces and logs attendance to CSV file
"""

import cv2
import os
import numpy as np
import csv
from datetime import datetime
from pathlib import Path
from config import *

class AttendanceSystem:
    def __init__(self):
        """Initialize the attendance system"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + CASCADE_PATH
        )
        
        # Create attendance file if it doesn't exist
        self.setup_attendance_file()
        
        # Dictionary to store detected faces
        self.detected_faces = {}
        self.frame_count = 0
        
    def setup_attendance_file(self):
        """Create attendance CSV file with headers if it doesn't exist"""
        if not os.path.exists(ATTENDANCE_DIR):
            os.makedirs(ATTENDANCE_DIR)
        
        if not os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Date', 'Time', 'Status'])
    
    def get_registered_faces(self):
        """Get list of registered face names"""
        if not os.path.exists(FACES_DATA_DIR):
            return []
        
        return [name for name in os.listdir(FACES_DATA_DIR) 
                if os.path.isdir(os.path.join(FACES_DATA_DIR, name))]
    
    def mark_attendance(self, name):
        """Mark attendance for a person"""
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
        # Check if already marked today
        with open(ATTENDANCE_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2 and row[0] == name and row[1] == date:
                    return False  # Already marked
        
        # Mark attendance
        with open(ATTENDANCE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time, 'Present'])
        
        return True
    
    def detect_faces_in_frame(self, frame):
        """Detect faces in the frame and return their regions"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_FACE_SIZE
        )
        return faces, gray
    
    def recognize_face(self, face_roi, registered_names):
        """
        Simple face recognition by comparing face region
        Returns the most similar registered face name
        """
        best_match = None
        best_similarity = 0
        
        for name in registered_names:
            name_dir = os.path.join(FACES_DATA_DIR, name)
            if not os.path.exists(name_dir):
                continue
            
            # Get average of registered faces
            registered_images = []
            for filename in os.listdir(name_dir):
                if filename.endswith('.jpg'):
                    img_path = os.path.join(name_dir, filename)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        img = cv2.resize(img, (face_roi.shape[1], face_roi.shape[0]))
                        registered_images.append(img)
            
            if not registered_images:
                continue
            
            # Calculate similarity using histogram comparison
            for reg_img in registered_images:
                hist1 = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([reg_img], [0], None, [256], [0, 256])
                
                similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
                # Lower value = better match for Bhattacharyya distance
                similarity = 1 - similarity
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = name
        
        if best_similarity > CONFIDENCE_THRESHOLD:
            return best_match, best_similarity
        
        return None, best_similarity
    
    def run(self):
        """Main loop for the attendance system"""
        cap = cv2.VideoCapture(CAMERA_ID)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        
        registered_names = self.get_registered_faces()
        
        if not registered_names:
            print("No registered faces found!")
            print("Please run register_face.py first to register faces")
            cap.release()
            return
        
        print(f"Registered faces: {', '.join(registered_names)}")
        print("Starting attendance system... (Press 'q' to quit)")
        
        marked_today = {}  # Track who's been marked today
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Flip frame for selfie view
                frame = cv2.flip(frame, 1)
                
                # Detect faces
                faces, gray = self.detect_faces_in_frame(frame)
                
                self.frame_count += 1
                
                for (x, y, w, h) in faces:
                    # Extract face region
                    face_roi = gray[y:y + h, x:x + w]
                    
                    # Recognize face
                    name, confidence = self.recognize_face(face_roi, registered_names)
                    
                    # Draw rectangle
                    color = (0, 255, 0) if name else (0, 0, 255)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    
                    if name:
                        label = f"{name} ({confidence:.2f})"
                        
                        # Mark attendance every N frames
                        if (self.frame_count % MARK_ATTENDANCE_EVERY_FRAMES == 0 and
                            name not in marked_today):
                            if self.mark_attendance(name):
                                marked_today[name] = True
                                print(f"✓ Attendance marked for {name}")
                    else:
                        label = f"Unknown ({confidence:.2f})"
                    
                    cv2.putText(
                        frame,
                        label,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        FONT_SCALE,
                        color,
                        TEXT_THICKNESS
                    )
                
                # Display status
                cv2.putText(
                    frame,
                    f"Marked: {len(marked_today)} | Frame: {self.frame_count}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SCALE,
                    (0, 255, 0),
                    TEXT_THICKNESS
                )
                
                cv2.imshow('Attendance System', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"\nAttendance system stopped.")
            print(f"Marked {len(marked_today)} people today")

if __name__ == "__main__":
    system = AttendanceSystem()
    system.run()
