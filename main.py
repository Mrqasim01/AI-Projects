"""
Main entry point for Face Detection Attendance System
"""

from gui.main_gui import AttendanceSystemGUI

def main():
    """Launch the GUI application"""
    app = AttendanceSystemGUI()
    app.run()

if __name__ == "__main__":
    main()
