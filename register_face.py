"""
Register new faces for the attendance system
Run this script to capture and register a new person's face
"""

import cv2
import os
from datetime import datetime
from config import *

def register_face(name, num_samples=30):
    """
    Capture multiple samples of a face for registration
    
    Args:
        name: Name of the person
        num_samples: Number of face samples to capture
    """
    
    # Create face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + CASCADE_PATH)
    
    # Open camera
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    # Create directory for the person if it doesn't exist
    person_dir = os.path.join(FACES_DATA_DIR, name)
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)
    
    print(f"Registering face for: {name}")
    print("Press 'c' to capture face sample, 'q' to quit")
    
    captured = 0
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=SCALE_FACTOR,
                minNeighbors=MIN_NEIGHBORS,
                minSize=MIN_FACE_SIZE
            )
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                
                # Add text
                cv2.putText(
                    frame,
                    f"Press 'c' to capture ({captured}/{num_samples})",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SCALE,
                    FONT_COLOR,
                    TEXT_THICKNESS
                )
            
            cv2.imshow(f"Registering: {name}", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c') and len(faces) > 0:
                # Save face image
                face_x, face_y, face_w, face_h = faces[0]
                face_roi = frame[face_y:face_y + face_h, face_x:face_x + face_w]
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(person_dir, f"{name}_{captured}_{timestamp}.jpg")
                cv2.imwrite(filename, face_roi)
                
                captured += 1
                print(f"✓ Captured sample {captured}/{num_samples}")
                
                if captured >= num_samples:
                    print(f"✓ Registration complete for {name}!")
                    break
            
            frame_count += 1
            
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    name = input("Enter the name of the person: ").strip()
    if name:
        num_samples = input("Enter number of face samples to capture (default 30): ").strip()
        num_samples = int(num_samples) if num_samples.isdigit() else 30
        register_face(name, num_samples)
    else:
        print("Name cannot be empty!")
