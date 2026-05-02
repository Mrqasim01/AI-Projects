## Quick Start Guide

### Installation & Setup

1. **Install Dependencies** (1-2 minutes):
```bash
pip install -r requirements.txt
```

All dependencies should install successfully now. The system will work with or without `face-recognition`.

2. **Run the Application**:
```bash
python main.py
```

### Login Credentials
- **Username:** qasim01
- **Password:** Qasim@2001

### First Time Use

1. **Register a Student:**
   - Click "Register Student"
   - Fill in: Roll Number, Name, Department, Email, Phone
   - Click "Capture Photo" (webcam will open)
   - Click "Register Student"

2. **Start Attendance:**
   - Click "Start Attendance"
   - Face detection begins in real-time
   - Recognized students are automatically marked present
   - Click "Stop Attendance" to end session

3. **View Records:**
   - Click "View Attendance"
   - Filter by date or student
   - Export to Excel

### System Capabilities

✅ **With face_recognition library** (advanced accuracy):
- Deep learning-based face recognition
- Higher accuracy for recognition
- Better handling of lighting conditions

✅ **Without face_recognition** (fallback mode):
- OpenCV Haar Cascade face detection
- Real-time face detection
- Suitable for basic attendance tracking

### Troubleshooting

**Problem: "Warning: face_recognition library not available"**
- This is OK! System uses fallback detection
- To install face_recognition (optional):
  - Windows: May require Visual C++ Build Tools
  - Linux/Mac: `pip install face-recognition`

**Problem: Camera not detected**
- Check camera permissions
- Try different camera index in code

**Problem: Application won't start**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (3.8+ required)

### File Structure

```
Face-Detection-Attendance/
├── main.py                      ← Run this to start
├── requirements.txt             ← Dependencies
├── gui/main_gui.py              ← GUI code
├── models/
│   ├── database_manager.py      ← Database operations
│   └── face_recognition_model.py ← Face recognition
├── database/attendance.db       ← SQLite database (auto-created)
└── images/                      ← Student photos
```

### Features

✨ **Core Features:**
- Student registration with photos
- Real-time face detection & recognition
- Automatic attendance marking
- Attendance reports & export to Excel
- Admin authentication

🔒 **Security:**
- Encrypted password storage
- Secure database
- Admin login required

📊 **Analytics:**
- Attendance statistics
- Charts and trends
- Date-based filtering

Enjoy using the Face Detection Attendance System!