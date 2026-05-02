"""
FastAPI server for Face Detection Attendance System
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import cv2
from datetime import datetime
import uvicorn
import shutil

from models.database_manager import DatabaseManager
from models.face_recognition_model import FaceRecognition

app = FastAPI(
    title="Face Detection Attendance System API",
    description="REST API for managing student attendance using face recognition",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize models
db = DatabaseManager()
face_recog = FaceRecognition()

# Pydantic models
class StudentCreate(BaseModel):
    roll_number: str
    full_name: str
    department: str
    email: str
    phone: str

class StudentResponse(BaseModel):
    roll_number: str
    full_name: str
    department: str
    email: str
    phone: str
    image_path: Optional[str]

class AttendanceRecord(BaseModel):
    roll_number: str
    full_name: str
    date: str
    time: str
    confidence: Optional[float]

class AttendanceStats(BaseModel):
    total_students: int
    today_attendance: int
    month_unique: int

@app.get("/", response_class=HTMLResponse)
async def root():
    """API documentation page"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Face Detection Attendance System API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
            code { background: #e8e8e8; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>Face Detection Attendance System API</h1>
        <p>FastAPI-powered REST API for managing student attendance using face recognition.</p>

        <h2>Available Endpoints:</h2>
        <ul>
            <li><strong>GET</strong> <code>/api/students</code> - Get all registered students</li>
            <li><strong>POST</strong> <code>/api/students</code> - Register new student with photo</li>
            <li><strong>GET</strong> <code>/api/attendance</code> - Get attendance records</li>
            <li><strong>POST</strong> <code>/api/attendance</code> - Mark attendance with face image</li>
            <li><strong>GET</strong> <code>/api/stats</code> - Get attendance statistics</li>
            <li><strong>GET</strong> <code>/docs</code> - Interactive API documentation</li>
        </ul>

        <h2>Quick Start:</h2>
        <p>Visit <a href="/docs">/docs</a> for interactive API documentation with examples.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/students", response_model=List[StudentResponse])
async def get_students():
    """Get all registered students"""
    try:
        students = db.get_all_students()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/students", response_model=dict)
async def register_student(
    roll_number: str = Form(...),
    full_name: str = Form(...),
    department: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    photo: UploadFile = File(...)
):
    """Register a new student with photo"""
    try:
        # Validate required fields
        if not all([roll_number, full_name, department, email, phone]):
            raise HTTPException(status_code=400, detail="All fields are required")

        # Save uploaded photo
        filename = f"student_{roll_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Add to database
        student_id = db.add_student(roll_number, full_name, department, email, phone)

        if student_id:
            # Register face encoding
            if face_recog.register_student_face(roll_number, filepath):
                return {
                    "message": f"Student {full_name} registered successfully",
                    "student_id": student_id
                }
            else:
                # Remove incomplete registration
                db.delete_student(roll_number)
                os.remove(filepath)
                raise HTTPException(status_code=400, detail="Face registration failed")
        else:
            os.remove(filepath)
            raise HTTPException(status_code=400, detail="Roll number already exists")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance", response_model=List[AttendanceRecord])
async def get_attendance(
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    roll_number: Optional[str] = Query(None, description="Filter by roll number")
):
    """Get attendance records"""
    try:
        records = db.get_attendance_records(date_filter=date, roll_filter=roll_number)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/attendance", response_model=dict)
async def mark_attendance(photo: UploadFile = File(...)):
    """Mark attendance using face recognition"""
    try:
        # Save temporary photo
        filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Recognize faces
        recognized_students = face_recog.recognize_faces(filepath)

        if not recognized_students:
            os.remove(filepath)
            raise HTTPException(status_code=400, detail="No faces recognized")

        # Mark attendance for recognized students
        marked = []
        for student_roll in recognized_students:
            if db.mark_attendance(student_roll):
                marked.append(student_roll)

        # Clean up temp file
        os.remove(filepath)

        return {
            "message": f"Attendance marked for {len(marked)} students",
            "recognized": recognized_students,
            "marked": marked
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats", response_model=AttendanceStats)
async def get_stats():
    """Get attendance statistics"""
    try:
        stats = db.get_attendance_stats()
        return AttendanceStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )