"""
Configuration file for Face Detection Attendance System
"""

# Camera settings
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Face detection settings
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_FACE_SIZE = (30, 30)

# Paths
FACES_DATA_DIR = 'faces'
ATTENDANCE_DIR = 'data'
CASCADE_PATH = 'haarcascade_frontalface_default.xml'

# Attendance settings
ATTENDANCE_FILE = 'data/attendance.csv'
MARK_ATTENDANCE_EVERY_FRAMES = 30  # Mark attendance every 30 frames
CONFIDENCE_THRESHOLD = 0.6

# Display settings
FONT_SCALE = 0.6
FONT_COLOR = (0, 255, 0)
TEXT_THICKNESS = 2
