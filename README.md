# Face Detection Attendance System

A professional Python-based real-time face detection and attendance management system with modern GUI.

## Features

- ✅ **Student Registration**: Complete student details with photo capture
- ✅ **Registered Students Management**: View, search, and manage registered students
- ✅ **Face Recognition**: Advanced face recognition using face_recognition library
- ✅ **Real-time Attendance**: Automatic attendance marking with confidence scores
- ✅ **Modern GUI**: CustomTkinter-based professional interface
- ✅ **Database Integration**: SQLite database for data persistence
- ✅ **Reports & Analytics**: Attendance statistics and export capabilities
- ✅ **Admin Authentication**: Secure login system
- ✅ **Email Notifications**: Automated attendance notifications
- ✅ **Responsive Design**: Dark/light theme support

## Installation

### Prerequisites
- Python 3.8+
- Webcam/Camera
- Windows/Linux/Mac

### Setup

1. **Clone or download this project**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Optional: Install face-recognition library for enhanced accuracy:**
```bash
pip install face-recognition
```
*Note: The face-recognition library provides better face recognition accuracy. The system will work without it but with limited face recognition capabilities.*

**Note:** `sqlite3` is a built-in Python module and doesn't need installation. The `face-recognition` library is optional - the system includes fallback face detection using OpenCV if it's not available.

3. **Run the application:**
```bash
python main.py
```

## Usage

### Admin Login
- **Default Username:** qasim01
- **Default Password:** ***********

### Student Registration
1. Login as admin
2. Click "Register Student"
3. Fill in student details (Roll Number, Name, Department, Email, Phone)
4. Capture photo using webcam
5. Click "Register Student"

### Starting Attendance
1. Click "Start Attendance"
2. The system will begin real-time face recognition
3. Recognized students will have attendance automatically marked
4. View live confidence scores and recognition status

### Viewing Attendance
1. Click "View Attendance"
2. Filter by date or roll number
3. Export records to Excel format

### Reports & Statistics
1. Click "Reports" to view attendance statistics
2. See charts for attendance trends
3. Monitor system performance

## Project Structure

```
Face-Detection-Attendance/
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
├── config.py                    # Legacy configuration (kept for compatibility)
├── register_face.py             # Legacy registration script
├── attendance_system.py         # Legacy attendance script
├── view_attendance.py           # Legacy view script
├── setup.py                     # Legacy setup script
├── data/                        # Legacy data directory
├── faces/                       # Legacy faces directory
├── images/                      # Student photos
├── attendance/                  # Attendance export files
├── database/                    # SQLite database files
├── gui/                         # GUI components
│   └── main_gui.py             # Main GUI application
└── models/                      # Business logic models
    ├── database_manager.py     # Database operations
    └── face_recognition_model.py # Face recognition logic
```

## Configuration

The system uses SQLite database (`database/attendance.db`) for data storage. Database is automatically created on first run.

### Face Recognition Settings
- **Tolerance:** 0.6 (lower = stricter matching)
- **Confidence Threshold:** 0.7 (minimum confidence for attendance marking)

## How It Works

1. **Registration**: Student photos are captured and face encodings are generated using face_recognition library
2. **Recognition**: Live video feed is processed to detect and recognize faces in real-time
3. **Attendance**: When a face is recognized with sufficient confidence, attendance is automatically marked
4. **Storage**: All data is stored in SQLite database with proper relationships
5. **Reports**: Attendance data can be viewed, filtered, and exported

## Security Features

- Admin authentication with password hashing
- Secure database storage
- Input validation and sanitization
- Error handling and logging

## Troubleshooting

**Camera Issues:**
- Ensure camera permissions are granted
- Try different camera indices in code
- Check camera compatibility

**Face Recognition Issues:**
- Ensure good lighting
- Register multiple angles of face
- Adjust confidence thresholds if needed

**Database Issues:**
- Check write permissions for database directory
- Ensure SQLite is available

**GUI Issues:**
- Ensure all dependencies are installed
- Try running with different Python versions
- Check CustomTkinter compatibility

## Future Enhancements

- [ ] Multi-camera support
- [ ] Mobile app integration
- [ ] Cloud backup
- [ ] Advanced analytics
- [ ] API endpoints
- [ ] Multi-language support
- [ ] Batch student import
- [ ] Attendance notifications via SMS

## Technology Stack

- **Frontend:** CustomTkinter (Modern Tkinter wrapper)
- **Backend:** Python 3.8+
- **Database:** SQLite
- **Computer Vision:** OpenCV, face_recognition
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib
- **Security:** bcrypt for password hashing

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.